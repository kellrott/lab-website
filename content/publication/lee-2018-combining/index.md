---
# Documentation: https://wowchemy.com/docs/managing-content/

title: 'Combining accurate tumor genome simulation with crowdsourcing to benchmark somatic structural variant detection'
subtitle: ''
summary: ''
authors:
- Anna Y Lee
- Adam D Ewing
- Kyle Ellrott
- Yin Hu
- Kathleen E Houlahan
- J Christopher Bare
- Shadrielle Melijah G Espiritu
- Vincent Huang
- Kristen Dang
- Zechen Chong
- Cristian Caloian
- Takafumi N Yamaguchi
- ICGC-TCGA DREAM Somatic Mutation Calling Challenge Participants
- Michael R Kellen
- Ken Chen
- Thea C Norman
- Stephen H Friend
- Justin Guinney
- Gustavo Stolovitzky
- David Haussler
- Adam A Margolin
- Joshua M Stuart
- Paul C Boutros
tags: []
categories: []
date: '2018-11-06'
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
abstract: 'The phenotypes of cancer cells are driven in part by somatic structural variants. Structural variants can initiate tumors, enhance their aggressiveness, and provide unique therapeutic opportunities. Whole-genome sequencing of tumors can allow exhaustive identification of the specific structural variants present in an individual cancer, facilitating both clinical diagnostics and the discovery of novel mutagenic mechanisms. A plethora of somatic structural variant detection algorithms have been created to enable these discoveries; however, there are no systematic benchmarks of them. Rigorous performance evaluation of somatic structural variant detection methods has been challenged by the lack of gold standards, extensive resource requirements, and difficulties arising from the need to share personal genomic information. To facilitate structural variant detection algorithm evaluations, we create a robust simulation framework for somatic structural variants by extending the BAMSurgeon algorithm. We then organize and enable a crowdsourced benchmarking within the ICGC-TCGA DREAM Somatic Mutation Calling Challenge (SMC-DNA). We report here the results of structural variant benchmarking on three different tumors, comprising 204 submissions from 15 teams. In addition to ranking methods, we identify characteristic error profiles of individual algorithms and general trends across them. Surprisingly, we find that ensembles of analysis pipelines do not always outperform the best individual method, indicating a need for new ways to aggregate somatic structural variant detection approaches. The synthetic tumors and somatic structural variant detection leaderboards remain available as a community benchmarking resource, and BAMSurgeon is available at https://github.com/adamewing/bamsurgeon .'
publication: '*Genome biology*'
doi: 10.1186/s13059-018-1539-5
pmid: '30400818'
---
