+++
title = "G2P Whitepaper"
date = 2018-09-09T13:56:34-07:00
draft = false

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors = ["Adam Margolin", "Josh Stuart", "Kyle Ellrott"]

# Tags and categories
# For example, use `tags = []` for no tags, or the form `tags = ["A Tag", "Another Tag"]` for one or more tags.
tags = ["GA4GH"]
categories = []

# Featured image
# Place your image in the `static/img/` folder and reference its filename below, e.g. `image = "example.jpg"`.
# Use `caption` to display an image caption.
#   Markdown linking is allowed, e.g. `caption = "[Image credit](http://example.org)"`.
# Set `preview` to `false` to disable the thumbnail in listings.
[header]
image = ""
caption = "A Whitepaper"
preview = true

+++

In 2014, Dr. Margolin, Dr. Stuart and Dr. Ellrott wrote a draft white paper outlining the need for a computational model to efficiently communicate known Genotype/Phenotype association. This working group would eventually evolve into Variant Interpretation for Cancer Consortium [VICC](http://cancervariants.org).

Many of the ideas and goals changed of the project changed over the years. Below is the original whitepaper draft, to show how much the project has evolved.


GA4GH Genotypes to Phenotypes (G2P) Task Team
---------------------------------------------

Motivation
One of the most important goals driving the collection of genome sequence information is to understand how particular variants lead to observable phenotypes and treatment options.
Yet no standards exist on how to describe genotype to phenotype (G2P) relationships. Several databases exist that have begun to collect G2P information such as PharmGKB, my cancer genome, MD Anderson’s personalized therapy knowledge base, ClinVar, SNPeff, OMIM, and the Human Gene Mutation Database. However, it is not possible to compare or aggregate data from these disparate sources because each use their own terminologies. Additionally, prediction of G2P relationships is an extremely active research area, with thousands of papers proposing novel signatures, biomarkers, and mathematical models to predict a given phenotype, and multiple crowd-sourced challenges soliciting thousands of models from the community around G2P problems such as prediction of breast cancer prognosis, response to rheumatoid arthritis therapy, and sensitivity of cancer cell lines to small molecular or shRNA treatments. Because no standards exist for representing such computationally derived predictions, it is difficult to compare the accuracy of different predictors for a given problem, leading to inconsistency and lack of clarity regarding bona-fide predictive signatures, and models trained on a given dataset are not easily applied to G2P prediction in related datasets, making it difficult to assess robustness or gain knowledge of signatures related to multiple phenotypes.

Other GA4GH working groups are creating standards for representing and computing on genetic and clinical (phenotype) data. We aim to build on and connect the work of these GA4GH groups, by defining standard data representations and building out a computable resource of G2P relationships. Formally, G2P relations may be described as a triple (see Goals for the API Specification) with Genotype(G), Phenotype(P) and Connection(C). Other GA4GH groups are defining standards for G and P, while our group will define standards for C.

A successful, long-term implementation would be able to represent G2P relationships derived from multiple sources, including those approved for clinical actionability, derived from the literature, or inferred from data analysis. This implementation would also represent both simple G2P relationships associated with a single genetic variant, as well as more complex G2P relationships in which phenotype is defined as a multi-variate function incorporating multiple omics data types and prior knowledge, such as pathway relationships.

Driving Pilot Projects
We propose pilot projects that initially implement the simpler use case (literature-derived, single variant relationships) while building up towards the more complex use case of computationally-derived multi-variate relationships.

Project 1. Extract genotype-to-phenotype information from the literature.
-------------------------------------------------------------------------

Our first driving project will build both the representation standards and initial implementation of a publicly available clinical genomics database derived from literature-based associations between a genetic variant and a phenotype. We will initially focus on cancer genetic variants linked to therapeutic response. We will then expand to represent genetic variants corresponding to risk or diagnostic markers of non-cancer genetic diseases.

Many efforts at cancer centers across the world are now focusing on developing a clinical genomics database to guide precision medicine treatment decisions. Therefore, we believe a GA4GH initiative could be of great benefit to the community, by defining standards to create compatibility across these multiple efforts, and creating an open community resource that will eliminate redundancy across efforts.

Our group will include leaders of prominent clinical genomics efforts, including: Gordon Mills, who leads MDAnderson’s personalized cancer therapy initiative (https://pct.mdanderson.org/); Chris Corless, who leads the Knight Diagnostic Lab at OHSU, and Rodrigo Dienstmann, who created the clinical genomics database for Massachussets General Hostpital. Taken together, these efforts have compiled hundreds of G2P associations, and proposed structured data representations. Once our project is formalized, we will reach out to other people leading prominent international clinical genomics efforts. Through discussions among these experts, we will create a representational standard that allows information across these databases to be merged. Clinical experts will work closely with professional engineers, from Google and elsewhere, to codify and implement agreed upon ideas into a computable resource.

Project 2. Compare literature derived biomarker / drug clinical associations with (simple) computationally inferred biomarker / drug response associations.
----------------------------------------

This project is designed to explore a simple example of connecting literature-derived associations from the clinical genomics database (project 1) to data-derived predictions from analysis of pharmacogenomic screens. We will utilize data from large-scale pharmacogenomic projects, including the Cancer Cell Line Encyclopedia (CCLE), Sanger Genomics of Drug Sensitivity (Sanger), and Broad’s Cancer Target Discovery and Development (CTDD) network screens. Each dataset contains several hundred cell lines with molecular characterization (gene expression, copy number, mutation) and sensitivity to a panel of compounds. Here we will begin by representing associations between mutations and sensitivity, calculated by simple univariate statistics, such as correlation.

We will standardize: 1) the representation of sample metadata (in collaboration with the GA4GH metadata group) across the clinical genomic database and the cell line samples; and 2) the representation of associations inferred from the literature (clinical genomics database) and computationally.

The driving scientific question will be to evaluate the consistency of literature-reported associations in cell line pharmacogenomic models, and to evaluate the tumor-type specificity of associations between genotype and drug response. That is, for all variant-drug response associations used in clinical decision making for a given tumor type, we will assess the correlation between the same variant and drug response across all other tumor types profiled in the cell line panel.

For each drug, X, used in cell line studies.
For each variant, V, reported in the clinical genomics database to be associated with response to drug X in tumor type Y.
Compute Corr_Y as the correlation in cell line studies between response to drug X and presence of variant V in tumor type Y.
Compute Corr_other as the correlation in cell line studies between response to drug X and presence of variant V in all tumor types other than Y.
(optionally) Compute Corr_subset as the correlation in cell line studies between response to drug X and presence of variant V in tumor types related to Y (e.g. other haematopoeitic cancers).

This study will yield the following scientific outputs:
By assessing the distribution of Corr_Y, we will determine the extent to which pharmacogenomic screens represent current clinically actionable G2P relationships.
By assessing the distribution of Corr_Y in subsets of tumor types, we will determine if pharmacogenomic screens are better models of G2P for certain classes of compounds (e.g. we might expect cell intrinsic signalling inhibitors to show signal in cell lines, but not those dependent on microenvironment interactions).
By comparing the distribution of Corr_Y to Corr_other we will determine the extent to which clinically actionable G2P relationships are tumor type dependent versus dependent on cell-type-independent genetic alterations.
By comparing the distribution of Corr_Y to Corr_subset we will recommend potential opportunities to expand the indication for a given drug to other tumor types.

In addition to meeting the technical goal of harmonizing G2P derived from literature and computation, we believe this will represent the most comprehensive study to date assessing the extent to which clinically actionable G2P associations are dependent on tumor type vs. pan-tumor genetic alterations. We believe this will provide valuable information on the feasibility of running genomically guided, cross-tissue-type clinical trials.

Project 3 -- Using data from the Beat-AML functional genomics program, develop an initial specification allowing: models to be trained on a given dataset; stored in a central system; queried for predictions in a new dataset; and re-trained on a different dataset.
-----------------------------------------------------


In project 3 we will tackle the problem of representing complex computationally inferred predictive models consisting of many variables and input data types. We will build this implementation using data from OHSU’s Beat-AML program -- which will ultimately collect data on 1,000 primary AML patient samples, including RNA-seq and whole exome sequencing, and ex vivo viability screens after treatment with 200 siRNAs and 100 small molecules. Data currently exists on ~100 patients and will grow at the rate of 200 additional patients per year, reaching 1,000 patients within 5 years.

The ongoing accrual of patient samples throughout the duration of the project provides an opportunity to perform prospective assessment of model predictions and iteratively refine models as new data is accrued. Moreover, the genomic profiling information generated for  patients enrolled in this study will be used to provide them with cutting-edge genomically guided treatment options. Therefore, this study provides an ideal use case for integrating information from the clinical genomics database (project 1) with computationally derived predictions on the same patients.
We envision that our model specification will borrow from or extend existing language independent machine learning APIs, such as the Google prediction API. We will assess and leverage such existing tools to create a standard model specification, including capabilities such as methods for train and predict, and structured representations of performance statistics such as cross validation accuracy. We envision that other aspects of the specification will be specific to G2P applications, including specifications for representing biomarkers or predictive signatures inferred by the model. Such a specification should be context-aware of the input data types, and thus able to represent biomarkers inferred at the gene level, data type level (e.g. mutation vs. copy number), or possibly pathway level. G2P associations inferred by such predictive models should be compatible with G2P association stored in the clinical genomics database, allowing comparison of computationally inferred predictors with those used in clinical care or reported in the literature.
Every 3 months roughly 50 new samples will be profiled by Beat-AML. We envision training a number of different models on all samples generated up to that point (excluding the 50 new samples) and storing a representation of each trained model, including cross validation performance statistics. Each model will then be used to predict sensitivity to each compound and siRNA in the 50 new samples, and the correlation between predicted vs. measured sensitivities will be computed in the new samples (i.e. the test accuracy). We will compare the cross validation accuracy to the test accuracy across all models. For models that achieve high test accuracy, we will query for inferred functional biomarkers, which will be: compared to associations in the clinical genomics database; functionally experimentally validated; and ultimately used to augment clinical reports to suggest additional treatment options for patients who have exhausted standard of care. Additionally, all models will be retrained, including the additional 50 samples, and assessed again based on the next batch of 50 samples, thus providing robustness statistics of model accuracy in multiple rounds of prospective assessment.

Project 4. Develop a library of predictors to connect tumor samples to phenotypic outcomes
------------------------------------------------------------------------------------------

We will develop a library of predictors that can be queried against to annotate new samples, such as those from the Beat-AML project described above. We will focus on the use of gene expression data, primarily RNA-Seq, as omics features to train machine-learning predictors. Identifying accurate predictors allows gene expression signatures to be used as surrogates for phenotypic (or even genotypic) events. Because a rich set of phenotypic information is more readily available from model systems such as cell lines and xenografts, it remains a challenge to connect the results found in these models to actual patient tumors. This project closes the gap by connecting tumor samples to outcomes using gene expression as the common comparator (in the same spirit as the Connective Map project). TCGA tumor samples will be connected to drug response and gene essentiality found in cell lines using the predictor library.

To this end, we will develop recognizers based on cell line models. For this, we will develop drug sensitivity predictors using all of the CCLE data.  In addition, we will use the Achilles dataset to develop predictors of gene essentiality across a diverse set of cell lines. We will then perform an all-against-all comparison of predictors trained on cell lines to those trained on TCGA samples.  For each prediction task, we will test a library of machine-learning classifiers for their accuracy on the defined outcome challenges. We will start with simple linear classifiers (or penalized versions) to populate the initial library. Only recognizers performing significantly better than chance, based on cross-validation performance, will be added to the library. Once added to the library, a background distribution will be constructed for every accurate recognizer using positive and negative samples not included in training. This will enable the detection of a case when a new sample is significantly “recognized” by an entry in the library as a sample with an extreme score on the background distribution. We will assess the biological significance of these inferences by checking the degree to which a set of positive control samples (e.g. HER2 breast cancer samples) are connected to the appropriate recognizers (HER2 inhibitor sensitivity recognizer).

In addition, we will populate the library with predictors trained from the TCGA datasets. Co-lead Stuart has led the TCGA Pan-Cancer project. A benchmark will be created with the current “Pan-Cancer-12” dataset, data from Sage Bionetwork’s TCGA Live collection, and later replaced with results from the Pan-Cancer-21. We will include predictors developed to predict mutation status for the most frequently mutated genes, expression-based subtypes within tumor types, expression-based subtypes across tumor types, and clinical outcomes within each tumor type. In a similar way as described for the cell line predictors, background distributions can be generated for accurate classifiers. We can then apply the recognizers back on to the cell line samples. This will give an important “reciprocal” view on the connections between the tumor sample and cell line data sets. We may find, that patients with a particular mutation (e.g. BRAF) are predicted to be sensitive to a similar drug (e.g. vemurafinib) by comparing the output of a tumor sample predictor (BRAF vs non-BRAF mutant) against a cell line predictor (vemerafinib sensitive vs resistant).

Once we establish the library and demonstrate its biological significance, we will develop an API allow querying from any tumor- or cell line-based predictor. We will test the utility by applying the library to the re-analysis of the Beat-AML samples described above.

Sharing Information Without Compromising Patient Privacy
A successful description would enable remote repositories to exchange G2P information without compromising patient privacy. Medical centers and hospitals are beginning to amass a large amount of genomics and functional genomics data along with other clinical and demographic information in patient records. Due to patient privacy concerns, protected health information (PHI) is kept behind firewalls to maintain compliance with state and federal laws. For routine care, this protection of data suffices. However, there are cases where it is vital to connect observations across institutions (e.g. to spot trends among patients with rare disorders). It could mean the difference between health and suffering for an institute to be able to share with another doctor (or parent) that a particular variant is predicted to be causal for a particular rare disease, is associated with several possible symptoms, and that several treatment strategies have been tried with varying degrees of success. See for example the story by Matt Might about his son Bertrand’s rare genetic disorder and how they only were able to track down other children with the disease because his blog went viral, due mainly to his blog’s prior popularity. In most cases it is nearly impossible for parents and doctors to make such connections.

Goals for the API specification.
The API will describe the types of G2P relations over which possible queries can be expressed. Relations will be described as a triple with Genotype(G), Phenotype(P) and Connection(C).  Since other working groups in the GA4GH are fleshing out G and P, this group is focused on the ontology specification for the method of connections C. The element G represents a data structure which would describe combinations of genomic location, genomic event type, gene symbol link, and a link to a sample. Furthermore, it would encompass other “omics” data to describe cellular and tissue states beyond the genotype such as copy number (e.g. from SNP6 chips), the transcriptome (e.g. RNA-seq vector of gene levels), epigenome (e.g. DNA methylation estimates), proteome (e.g. reverse-phase protein arrays), metabolome, and so on,  If any of those elements is omitted, it is treated as a wildcard, ie if a gene like TP53 is defined, with a genomic event as MUTATION, but no sample defined, it matches all samples with TP53 mutations.

The API would allow the user to query using a chain of triple statements, where a subset of each triples items is a some sort of selection operation, such as a wildcards or comparison operators. In the following examples, each triple is in the order (G, P, C):

To motivate the discussion, consider the following several use cases:

Use Case 1 - Given a specific phenotype of interest (e.g. cardiomyopathy, cancer subtype, drug sensitivity, etc) list all genes with a non-synonymous mutation in a sample w/ the phenotype. UC1 is a query of the type `(*,*,P)` which gives all genotypes associated with a phenotype no matter what the method was that determined the connection.

Use Case 2 - (inverse to UC1) - Given a specific variant in a particular gene, list all phenotypes observed with specific evidence code (e.g. inferred author statement, direct assay, predicted by gene expression classifier, etc). UC2 is a query of the type (G,*,*) which gives all phenotypes associated with a phenotype no matter what the method was that determined the connection.

Use Case 3 - Given a (genotype, phenotype) pair such as (V600E in BRAF, responsive to vemurafinib) return if and what kind of evidence supports the association (e.g. clinical trial <CLINICAL TRIAL ID>). UC3 is a query of the type (G, C_clinicaltrial, P), that uses a defined comparison function to find clinical trials edges.

Use Case 4 - Given a gene of interest A, are there events in any other genes B that are mutually exclusive with events in A across a specified cohort (or several cohorts). UC4 would be coded as MutuallyExclusive( [ `(G_geneA, C_belongs, P_cohort)`, `(*, C_belongs, P_cohort)` ] ), where `G_geneA` selects genomic events related to gene A, `C_belongs` is the predicate defines that a genotypes sample belongs to a particular cohort, P_cohort, and the second selection connect all variants also connected to that cohort. The function 'MutuallyExclusive' takes the selection and finds genes that are mutually exclusive in occurrence across samples. These kinds of server side functions allow the users to do statistical analysis across cohorts without having to transfer all of the data across the network.

Use Case 5 - Similar to UC4 - Are there other genes B that have events that are coincident with events of a particular kind in gene A? UC5 would be coded as `Correlated( [ (G_geneA, C_belongs, P_cohort)`, `(*, C_belongs, P_cohort) ], 0.9 )` which would list all Genes in the sample cohort with a correlation above 0.9.

Use Case 6 - Given a sample’s specific combination of variants and/or omics profiles, return the most associated phenotypes (predicted or assayed). UC6 would be coded as `MaxLink_P( [ G_gene1, *, * ], [ G_gene2, *, *], …, [G_geneN, *, *] )`, where the would be an N element description profiling the genomic elements of query, and `MapLink_P` would find the top hits that match these genomic features.

Appendix A -- Engineering notes
We feel that the best way to represent large scale relational data would be through the use a of Graph Database. SQL based systems are inflexible and hard to evolve, while also being very difficult to scale onto distributed systems. The alternative to SQL, key-value or document based NoSQL systems, are flexible and scale well, but most NoSQL based datastores only have soft relational data constructs. Graph Databases have many of the NoSQL benefits, the flexibility to deal with changing requirements, the ability to distribute data and scale horizontally while maintaining relationships as a core construct in the data store.

Such a system would be easy to design against, and would be ready for continually evolving data relationships. Most ontological descriptions of phenotypes would be available in RDF (http://www.bioontology.org/), and many biological projects already distribute data in this graph based format (ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/rdf/ http://bio2rdf.org/).

RDF is a triple based graph description. This means that the entire graph is described in statements or 'source node A connects via edge type B to node C'. This means that the resulting graph is only composed of nodes and edges. This graph model is much simpler then a full property graph, where each node and edge is allowed to have a set of key/value pairs attached to it. For dense genomic data a property graph would be a more concise way of describing complex relationships that involve many properties, coefficients and edge weights.
We also believe that it is important to not only define the data transfer standards but the APIs to make remote interrogation of the data available.

There exists APIs for graph queries, such as SPARQL, which have been designed directly for RDF. However this system does not directly apply to the property based graphs we have proposed using. Our work with Graph Databases indicate that Gremlin may be more in line with the idea of a property graph based system. In addition, gremlin has already been shown to be easily convertable to a Map-Reduce based architecture (http://thinkaurelius.github.io/faunus/ https://github.com/kellrott/sparkgraph), so it will be easier to scale to extremely large datasets.
