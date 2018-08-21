+++
title = "Handling Failures from OpenStack Swift in Funnel"

date = 2016-04-20T00:00:00
lastmod = 2018-01-13T00:00:00
draft = false

tags = ["development"]
summary = "Testing network errors."

+++

Handling Failures from OpenStack Swift in Funnel
When building distributed services, handling failures from other services is a fact of life.

We use OpenStack Swift as our object storage service, and we use Funnel to transfer thousands of objects to and from Swift. Failed transfers have been common; the Swift server ca be unavailable, overloaded, and even lose chunks of data during upload.

It’s been challenging to make Funnel tolerant to all these failures, improved our logs and tools available for debugging, improved our code, and we’ve learned a lot along the way.

Retries
At the core of handling failures is being able to retry failed requests.

In Funnel, we retry most failed requests to external services. We do this by wrapping our APIs in a generic utility which can replay the same request until it succeeds. For example,

```
// Storage is the interface we want to wrap.
type Storage interface {
  Put(sourcePath, destURL string) error
}

// NewStorageRetrier creates a wrapper around Storage which includes retry logic.
func NewStorageRetrier(backend Storage) *StorageRetrier {
  return StorageRetrier{
    Backend: backend,
    Retrier: util.Retrier{

      // At first, retry after one second.
      InitialInterval:     time.Second,

      // Each successive retry will wait twice as long before retrying.
      Multiplier:          2.0,

      // Retry for up to an hour.
      MaxElapsedTime:      60*time.Minute,

      // ShouldRetry decides whether the error can be retried.
      ShouldRetry: func(err error) bool {
        switch err {
        // Retry if the uploaded object isn't the same,
        // the service is unavailable, etc.
        case swift.ObjectCorrupted, swift.TimeoutError, swift.UnavailableError:
          return true
        default:
          return false
        }
      },
    },
  }
}
```

The code here is simplified for this post, the real code is here.

Our storage code will now attempt to upload the file multiple times until it succeeds. Funnel will try hard to upload, retrying for up to an hour.

Testing
The hard part about debugging failures is that they are often intermittent and difficult to reproduce.

Setting up a system which can deterministically reproduce specific types of failures takes some work, but it can be very useful and may be worth the price of admission.

Luckily, there are tools out there to help.

toxy
toxy is a proxy server which can be configured to inject errors into network traffic.

```
var toxy = require('toxy')
var poisons = toxy.poisons
var rules = toxy.rules
var proxy = toxy()

// Forward traffic to the actual Swift server
proxy.forward('http://swift.actual:8080')

// Inject "Object corrupted" errors into uploads,
// which happens when the uploaded object doesn't match
// the file being uploaded (meaning something got lost).
proxy
  .put('/*/buchanan/funnel-test/object-corrupted')
  .poison(poisons.inject({
    code: 200,
    // Change the object's etag (checksum) in the response to the PUT.
    //
    // This is how swift communicates to the client the checksum of the
    // object that was uploaded, so we force it to be corrupt here.
    headers: {'ETag': 'zzzzzzzzzf1a4e663f02245d42832766'}
  }))
  // Only corrupt the object 60% of the time.
  .withRule(rules.probability(60))

// Simulate the service being unavailable.
proxy
  .all('/*/buchanan/funnel-test/service-unavailable')
  .poison(poisons.inject({
    code: 503,
    body: '{"error": "toxy injected error"}',
    headers: {'Content-Type': 'application/json'}
  }))
  .withRule(rules.probability(60))

proxy.all("/*")
proxy.listen(8000)
```

The code above will proxy Swift traffic, injecting errors into traffic 60% of the time.

The failures can be accessed by pointing Funnel’s Swift client to this proxy, and uploading to a specific object URL:

```
export FUNNEL_SWIFT_STORAGE_URL=http://fake.swift:8000/v1/AUTH_abcedfg
funnel storage put swift://buchanan/funnel-test/service-unavailable
```

Now we can tweak the proxy errors and fix Funnel code at the same time, easily working out the kinks in error handling, and having confidence that Funnel is retrying requests correctly.

Retry screenshot

tcpdump
tcpdump allows you to monitor network traffic and inspect low-level packets. Incredibly useful for figuring out what’s going on with Swift and getting the proxy set up.

sudo tcpdump -n not port 22 and not icmp and not arp
This article does a great job at explaining the power of tcpdump.

iptables
At first, I wasn’t easily able to forward Funnel’s traffic to the Swift proxy via configuration alone, so I dug into Linux’s network layer using iptables to forward traffic to the proxy server.

iptables is an intimdating and complex tool, but also extremely powerful and capable of routing traffic almost anyway you can imagine.

The rule below watch for traffic going out to the actual Swift server (at 1.2.3.4:8080) and rewrites the IP address to point to the proxy instead (at 9.8.7.6:8080).

sudo iptables -t nat -A OUTPUT -p tcp -d 1.2.3.4 --dport 8080 -j DNAT --to-destination 9.8.7.6
This article does a decent job of introducing iptables.
