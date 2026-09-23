---
# Documentation: https://wowchemy.com/docs/managing-content/

title: 'Germline contamination and leakage in whole genome somatic single nucleotide variant detection'
subtitle: ''
summary: ''
authors:
- Dorota H Sendorek
- Cristian Caloian
- Kyle Ellrott
- J Christopher Bare
- Takafumi N Yamaguchi
- Adam D Ewing
- Kathleen E Houlahan
- Thea C Norman
- Adam A Margolin
- Joshua M Stuart
- Paul C Boutros
tags: []
categories: []
date: '2018-01-31'
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
abstract: 'The clinical sequencing of cancer genomes to personalize therapy is becoming routine across the world. However, concerns over patient re-identification from these data lead to questions about how tightly access should be controlled. It is not thought to be possible to re-identify patients from somatic variant data. However, somatic variant detection pipelines can mistakenly identify germline variants as somatic ones, a process called "germline leakage". The rate of germline leakage across different somatic variant detection pipelines is not well-understood, and it is uncertain whether or not somatic variant calls should be considered re-identifiable. To fill this gap, we quantified germline leakage across 259 sets of whole-genome somatic single nucleotide variant (SNVs) predictions made by 21 teams as part of the ICGC-TCGA DREAM Somatic Mutation Calling Challenge. The median somatic SNV prediction set contained 4325 somatic SNVs and leaked one germline polymorphism. The level of germline leakage was inversely correlated with somatic SNV prediction accuracy and positively correlated with the amount of infiltrating normal cells. The specific germline variants leaked differed by tumour and algorithm. To aid in quantitation and correction of leakage, we created a tool, called GermlineFilter, for use in public-facing somatic SNV databases. The potential for patient re-identification from leaked germline variants in somatic SNV predictions has led to divergent open data access policies, based on different assessments of the risks. Indeed, a single, well-publicized re-identification event could reshape public perceptions of the values of genomic data sharing. We find that modern somatic SNV prediction pipelines have low germline-leakage rates, which can be further reduced, especially for cloud-sharing, using pre-filtering software.'
publication: '*BMC bioinformatics*'
doi: 10.1186/s12859-018-2046-0
pmid: '29385983'
---
