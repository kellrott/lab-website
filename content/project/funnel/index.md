+++
# Date this page was created.
date = 2016-04-27T00:00:00
show_date = false

# Project title.
title = "Funnel"

# Project summary to display on homepage.
summary = "Funnel Task Execution Server"

# Optional image to display on homepage (relative to `static/img/` folder).
image_preview = "funnel.png"

# Tags: can be used for filtering projects.
# Example: `tags = ["machine-learning", "deep-learning"]`
tags = ["Data Systems"]

# Optional external URL for project (replaces project detail page).
external_link = "https://ohsu-comp-bio.github.io/funnel/"

# Does the project detail page use math formatting?
math = false

# Optional featured image (relative to `static/img/` folder).
[header]
image = "headers/bubbles-wide.jpg"
caption = "My caption :smile:"

+++

https://ohsu-comp-bio.github.io/funnel/

Funnel is a toolkit for distributed task execution with a simple API.

A task describes metadata, state, input/output files, resource requests, commands, and logs. The task API has four actions: create, get, list, and cancel. Given a task, Funnel will queue it, schedule it to a worker, and track its state and logs. A worker will download input files, run a sequence of Docker containers, upload output files, and emits events and logs along the way.

A wide variety of options make Funnel easily adaptable:
- BoltDB
- Elasticsearch
- MongoDB
- AWS Batch, S3, DynamoDB
- OpenStack Swift
- Google Cloud Storage, Datastore
- Kafka
- HPC support: HTCondor, Slurm, etc.
- and more
