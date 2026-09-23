---
# Documentation: https://wowchemy.com/docs/managing-content/

title: 'Identifying transcription factor binding sites through Markov chain optimization'
subtitle: ''
summary: ''
authors:
- Kyle Ellrott
- Chuhu Yang
- Frances M Sladek
- Tao Jiang
tags: []
categories: []
date: '2002-01-01'
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
abstract: 'Even though every cell in an organism contains the same genetic material, each cell does not express the same cohort of genes. Therefore, one of the major problems facing genomic research today is to determine not only which genes are differentially expressed and under what conditions, but also how the expression of those genes is regulated. The first step in determining differential gene expression is the binding of sequence-specific DNA binding proteins (i.e. transcription factors) to regulatory regions of the genes (i.e. promoters and enhancers). An important aspect to understanding how a given transcription factor functions is to know the entire gamut of binding sites and subsequently potential target genes that the factor may bind/regulate. In this study, we have developed a computer algorithm to scan genomic databases for transcription factor binding sites, based on a novel Markov chain optimization method, and used it to scan the human genome for sites that bind to hepatocyte nuclear factor 4 alpha (HNF4alpha). A list of 71 known HNF4alpha binding sites from the literature were used to train our Markov chain model. By looking at the window of 600 nucleotides around the transcription start site of each confirmed gene on the human genome, we identified 849 sites with varying binding potential and experimentally tested 109 of those sites for binding to HNF4alpha. Our results show that the program was very successful in identifying 77 new HNF4alpha binding sites with varying binding affinities (i.e. a 71% success rate). Therefore, this computational method for searching genomic databases for potential transcription factor binding sites is a powerful tool for investigating mechanisms of differential gene regulation.'
publication: '*Bioinformatics (Oxford, England)*'
doi: 10.1093/bioinformatics/18.suppl_2.s100
pmid: '12385991'
---
