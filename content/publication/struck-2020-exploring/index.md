---
# Documentation: https://wowchemy.com/docs/managing-content/

title: 'Exploring Integrative Analysis Using the BioMedical Evidence Graph'
subtitle: ''
summary: ''
authors:
- Adam Struck
- Brian Walsh
- Alexander Buchanan
- Jordan A Lee
- Ryan Spangler
- Joshua M Stuart
- Kyle Ellrott
tags: []
categories: []
date: '2020-02-01'
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
abstract: 'The analysis of cancer biology data involves extremely heterogeneous data sets, including information from RNA sequencing, genome-wide copy number, DNA methylation data reporting on epigenetic regulation, somatic mutations from whole-exome or whole-genome analyses, pathology estimates from imaging sections or subtyping, drug response or other treatment outcomes, and various other clinical and phenotypic measurements. Bringing these different resources into a common framework, with a data model that allows for complex relationships as well as dense vectors of features, will unlock integrated data set analysis. We introduce the BioMedical Evidence Graph (BMEG), a graph database and query engine for discovery and analysis of cancer biology. The BMEG is unique from other biologic data graphs in that sample-level molecular and clinical information is connected to reference knowledge bases. It combines gene expression and mutation data with drug-response experiments, pathway information databases, and literature-derived associations. The construction of the BMEG has resulted in a graph containing > 41 million vertices and 57 million edges. The BMEG system provides a graph query-based application programming interface to enable analysis, with client code available for Python, Javascript, and R, and a server online at bmeg.io. Using this system, we have demonstrated several forms of cross-data set analysis to show the utility of the system. The BMEG is an evolving resource dedicated to enabling integrative analysis. We have demonstrated queries on the system that illustrate mutation significance analysis, drug-response machine learning, patient-level knowledge-base queries, and pathway level analysis. We have compared the resulting graph to other available integrated graph systems and demonstrated the former is unique in the scale of the graph and the type of data it makes available.'
publication: '*JCO clinical cancer informatics*'
doi: 10.1200/CCI.19.00110
pmid: '32097025'
---
