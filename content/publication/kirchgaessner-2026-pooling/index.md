---
# Documentation: https://wowchemy.com/docs/managing-content/

title: 'Pooling multimodal cancer data across unaligned embedding spaces maintains tumor of origin signal'
subtitle: ''
summary: ''
authors:
- Raphael Kirchgaessner
- Kaya Keutler
- Shruthilayaa Sivakumar
- Xubo Song
- Kyle Ellrott
tags: []
categories: []
date: '2026-01-01'
lastmod: 2026-09-23T23:37:13.107169Z
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ''
  focal_point: ''
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []
publishDate: '2026-09-23T23:37:13.107169Z'
publication_types:
- '2'
abstract: 'AI-based embeddings offer the possibilities of encoding complex biological data into low-dimensional spaces, called embedding spaces, that maintain the relationships between entities. Vector pooling is the process of aggregating an array of embedded vectors, either usually by summing or averaging, to summarize the total movement with the embedding space. Embedded vector pooling allows sampling of an arbitrary number of points to be summarized into a fixed sized vector, and is frequently used to sample networks of embedded values or to summarize protein language model vectors. There is an open question about the compatibility of embedding spaces that are created without any coordination. It has been assumed that signals in these unaligned embedding spaces would be destroyed if vectors were pooled into summed values. To challenge this idea, we created a number of benchmarks that utilized unaligned embedded values and pooled them into heterogeneous vectors to test information retrieval. To power this benchmark, we trained embedding models across different cancer data modalities and tested how well pooled heterogeneous vectors were able to retain biologically relevant information. Our research shows that signal from unaligned embedded values is conserved and able to still be used for learning tasks, such as data modality and tumor of origin recognition. All code and computational experiments related to this publication can be found at https://github.com/EllrottLab/heterogeneous-embedding-vectors.'
publication: '*Bioinformatics advances*'
doi: 10.1093/bioadv/vbag159
pmid: '42534439'
---
