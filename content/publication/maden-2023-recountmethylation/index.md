---
# Documentation: https://wowchemy.com/docs/managing-content/

title: 'recountmethylation enables flexible analysis of public blood DNA methylation array data'
subtitle: ''
summary: ''
authors:
- Sean K Maden
- Brian Walsh
- Kyle Ellrott
- Kasper D Hansen
- Reid F Thompson
- Abhinav Nellore
tags: []
categories: []
date: '2023-01-01'
lastmod: 2026-09-23
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
publishDate: '2026-09-23'
publication_types:
- '2'
abstract: 'Thousands of DNA methylation (DNAm) array samples from human blood are publicly available on the Gene Expression Omnibus (GEO), but they remain underutilized for experiment planning, replication and cross-study and cross-platform analyses. To facilitate these tasks, we augmented our recountmethylation R/Bioconductor package with 12 537 uniformly processed EPIC and HM450K blood samples on GEO as well as several new features. We subsequently used our updated package in several illustrative analyses, finding (i) study ID bias adjustment increased variation explained by biological and demographic variables, (ii) most variation in autosomal DNAm was explained by genetic ancestry and CD4+ T-cell fractions and (iii) the dependence of power to detect differential methylation on sample size was similar for each of peripheral blood mononuclear cells (PBMC), whole blood and umbilical cord blood. Finally, we used PBMC and whole blood to perform independent validations, and we recovered 38-46% of differentially methylated probes between sexes from two previously published epigenome-wide association studies. Source code to reproduce the main results are available on GitHub (repo: recountmethylation_flexible-blood-analysis_manuscript; url: https://github.com/metamaden/recountmethylation_flexible-blood-analysis_manuscript). All data was publicly available and downloaded from the Gene Expression Omnibus (https://www.ncbi.nlm.nih.gov/geo/). Compilations of the analyzed public data can be accessed from the website recount.bio/data (preprocessed HM450K array data: https://recount.bio/data/remethdb_h5se-gm_epic_0-0-2_1589820348/; preprocessed EPIC array data: https://recount.bio/data/remethdb_h5se-gm_epic_0-0-2_1589820348/). Supplementary data are available at Bioinformatics Advances online.'
publication: '*Bioinformatics advances*'
doi: 10.1093/bioadv/vbad020
pmid: '36874953'
---
