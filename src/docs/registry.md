# LinkML Registry Entries

## LinkML Schema Metamodel

The metamodel for schemas defined using the Linked Data Modeling Language framework.

For more information on LinkML:

* [linkml.io](https://linkml.io) main website
* [specification](https://w3id.org/linkml/docs/specification/)

LinkML is self-describing. Every LinkML schema consists of elements
that instantiate classes in this metamodel.

Core metaclasses:

* [SchemaDefinition](https://w3id.org/linkml/SchemaDefinition)
* [ClassDefinition](https://w3id.org/linkml/ClassDefinition)
* [SlotDefinition](https://w3id.org/linkml/SlotDefinition)
* [TypeDefinition](https://w3id.org/linkml/TypeDefinition)

There are many subsets of *profiles* of the metamodel, for different purposes:

* [MinimalSubset](https://w3id.org/linkml/MinimalSubset)
* [BasicSubset](https://w3id.org/linkml/BasicSubset)
* [BasicSubset](https://w3id.org/linkml/BasicSubset)

For canonical reference documentation on any metamodel construct,
refer to the official URI for each construct, e.g.
[https://w3id.org/linkml/is_a](https://w3id.org/linkml/is_a)


|key|value|
| :---: | :---: |
|name|LinkML Model|
|title|LinkML Schema Metamodel|
|homepage|[https://linkml.github.io/linkml-model/docs/](https://linkml.github.io/linkml-model/docs/)|
|schema_url|[https://github.com/linkml/linkml-model/blob/main/model/schema/meta.yaml](https://github.com/linkml/linkml-model/blob/main/model/schema/meta.yaml)|
|github_repo|linkml/linkml-model|
|schema_relative_path|linkml_model/model/schema/meta.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|meta|
|class_count|41|
|slot_count|220|
|enum_count|4|
|type_count|19|
|proportion_elements_with_a_description|0.96|
|proportion_elements_mapped|0.29|

## LinkML template configuration

None


|key|value|
| :---: | :---: |
|name|LinkML Template Configuration Model|
|title|LinkML template configuration|
|homepage|[https://linkml.github.io/template-config-model/](https://linkml.github.io/template-config-model/)|
|schema_url|[https://github.com/linkml/template-config-model/blob/main/model/schema/config_model.yaml](https://github.com/linkml/template-config-model/blob/main/model/schema/config_model.yaml)|
|github_repo|linkml/template-config-model|
|license|CC-0|
|topics|meta|

## NMDC Schema

Schema for National Microbiome Data Collaborative (NMDC).
This schema is organized into multiple modules, such as:

 * a set of core types for representing data values
 * a subset of the mixs schema
 * an annotation schema
 * the NMDC schema itself, into which the other modules are imported


|key|value|
| :---: | :---: |
|name|NMDC|
|title|NMDC Schema|
|homepage|[https://microbiomedata.github.io/nmdc-schema/](https://microbiomedata.github.io/nmdc-schema/)|
|github_repo|microbiomedata/nmdc-schema|
|schema_relative_path|src/schema/nmdc.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|environmental microbiology|
|class_count|69|
|slot_count|864|
|enum_count|124|
|type_count|24|
|proportion_elements_with_a_description|0.74|
|proportion_elements_mapped|0.5|

## Biolink Model

Entity and association taxonomy and datamodel for life-sciences data


|key|value|
| :---: | :---: |
|name|Biolink-Model|
|title|Biolink Model|
|homepage|[https://biolink.github.io/biolink-model/](https://biolink.github.io/biolink-model/)|
|github_repo|biolink/biolink-model|
|schema_relative_path|biolink-model.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|genomics; disease; phenotype; expression; GO; GO-CAM; human biology; model organism biology; biochemistry; biology|
|class_count|302|
|slot_count|460|
|enum_count|19|
|type_count|32|
|proportion_elements_with_a_description|0.72|
|proportion_elements_mapped|0.38|

## Simple Standard Sharing Object Mappings

Datamodel for Simple Standard for Sharing Ontological Mappings (SSSOM)


|key|value|
| :---: | :---: |
|name|SSSOM|
|title|Simple Standard Sharing Object Mappings|
|homepage|[https://mapping-commons.github.io/sssom/](https://mapping-commons.github.io/sssom/)|
|github_repo|mapping-commons/SSSOM|
|schema_relative_path|src/sssom_schema/schema/sssom_schema.yaml|
|license|CC-0|
|topics|information; mappings|
|class_count|5|
|slot_count|71|
|enum_count|3|
|type_count|20|
|proportion_elements_with_a_description|0.96|
|proportion_elements_mapped|0.39|

## Knowledge Graph Change Language

A data model for describing change operations at a high level on an ontology or ontology-like artefact, such as a Knowledge Graph.

* [Browse Schema](https://cmungall.github.io/knowledge-graph-change-language/)
* [GitHub](https://github.com/cmungall/knowledge-graph-change-language)


|key|value|
| :---: | :---: |
|name|KGCL|
|title|Knowledge Graph Change Language|
|homepage|[https://cmungall.github.io/knowledge-graph-change-language/](https://cmungall.github.io/knowledge-graph-change-language/)|
|github_repo|cmungall/knowledge-graph-change-language|
|schema_relative_path|src/schema/kgcl.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|knowledge graphs|
|class_count|71|
|slot_count|70|
|enum_count|2|
|type_count|21|
|proportion_elements_with_a_description|0.74|
|proportion_elements_mapped|0.23|

## Knowledge Graph Visualization Configuration

A data model for describing configurations / stylesheets for visualzing graphs, and
in particular Knowledge Graphs or Ontologies. These graphs are characterized by having meaningful edge labels,
node categories, IDs or URIs on each element, as well as additional rich metadata on the nodes or edges.

An example of a use of this is https://github.com/INCATools/obographviz


|key|value|
| :---: | :---: |
|name|KGViz|
|title|Knowledge Graph Visualization Configuration|
|homepage|[https://berkeleybop.github.io/kgviz-model/](https://berkeleybop.github.io/kgviz-model/)|
|github_repo|berkeleybop/kgviz-model|
|schema_relative_path|src/kgviz_model/linkml/kgviz.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|visualization|
|class_count|16|
|slot_count|31|
|enum_count|3|
|type_count|21|
|proportion_elements_with_a_description|0.57|
|proportion_elements_mapped|0.32|

## Semantic SQL

A datamodel for RDF, OWL, and OBO Ontologies designed to work harmoniously with SQL databases.

Note that the primary purpose of this linkml schema is to organize and define SQL VIEWs to
be used on top of a generic SQL database following the rdftab statements schema.
These SQL views are encoded with the `sqlviews>>` tag inside the yaml.

We use linkml to do this rather than a simple SQL DDL file because linkml gives
us a standard way to do things such as:

  * attach descriptions to each view
  * define a data dictionary of all columns used, together with domains/ranges
  * modular structure with imports
  * the ability to attach rich semantic metadata to each schema element

Additionally, the framework provides automatic compilation to SQLAlchemy models,
and tools for being able to turn views into indexed tables for efficient querying,
as well as a rich searchable documentation system and other tooling.

This schema is best browsed online: https://cmungall.github.io/semantic-sql/

Note that things are in flux, and there some oddities that need ironed out, see
issues for details.

See the [github repo](https://github.com/cmungall/semantic-sql) for code to convert
from the linkml yaml into SQL DDL


|key|value|
| :---: | :---: |
|name|Semantic Sql|
|title|Semantic SQL|
|homepage|[https://cmungall.github.io/semantic-sql/](https://cmungall.github.io/semantic-sql/)|
|github_repo|cmungall/semantic-sql|
|schema_relative_path|src/semsql/linkml/semsql.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|ontologies|
|class_count|103|
|slot_count|34|
|enum_count|0|
|type_count|21|
|proportion_elements_with_a_description|0.54|
|proportion_elements_mapped|0.27|

## Chemical Entities Mixtures and Reactions Ontological Framework

A data model for managing information about chemical entities, ranging from atoms
through molecules to complex mixtures.

Aspects of this have been cribbed from various sources including CHEBI, SIO,
Wikipedia/Wikidata, the NCATS Translator Chemical Working Group, but all mistakes
are my own.

For full context/motivation see the [GitHub repo](https://github.com/chemkg/chemrof).


|key|value|
| :---: | :---: |
|name|Chemical Entities and Mixtures Model|
|title|Chemical Entities Mixtures and Reactions Ontological Framework|
|homepage|[https://chemkg.github.io/chemrof/](https://chemkg.github.io/chemrof/)|
|github_repo|chemkg/chemrof|
|schema_relative_path|src/schema/chemrof.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|chemistry|
|class_count|126|
|slot_count|217|
|enum_count|9|
|type_count|27|
|proportion_elements_with_a_description|0.54|
|proportion_elements_mapped|0.19|

## CRDC-H Model

None


|key|value|
| :---: | :---: |
|name|CCDH|
|title|CRDC-H Model|
|homepage|[https://cancerdhc.github.io/ccdhmodel](https://cancerdhc.github.io/ccdhmodel)|
|github_repo|cancerdhc/ccdhmodel|
|schema_relative_path|model/schema/crdch_model.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|cancer|
|class_count|41|
|slot_count|0|
|enum_count|106|
|type_count|26|
|proportion_elements_with_a_description|0.98|
|proportion_elements_mapped|0.15|

## common association file formats

None


|key|value|
| :---: | :---: |
|name|ontology-associations|
|title|common association file formats|
|homepage|[https://biodatamodels.github.io/ontology-associations/](https://biodatamodels.github.io/ontology-associations/)|
|github_repo|biodatamodels/ontology-associations|
|license|CC-0|
|topics|genomics|

## Genome Feature Format LinkML rendering

Playing around with GFF spec


|key|value|
| :---: | :---: |
|name|GFF3|
|title|Genome Feature Format LinkML rendering|
|homepage|[https://biodatamodels.github.io/gff-schema/](https://biodatamodels.github.io/gff-schema/)|
|github_repo|biodatamodels/gff-schema|
|schema_relative_path|src/schema/gff.yaml|
|license|CC-0|
|topics|genomics|
|class_count|8|
|slot_count|26|
|enum_count|3|
|type_count|21|
|proportion_elements_with_a_description|0.67|
|proportion_elements_mapped|0.43|

## Chromosome ontology and ETL

None


|key|value|
| :---: | :---: |
|name|Monochrom|
|title|Chromosome ontology and ETL|
|homepage|[https://monarch-initiative.github.io/monochrom/](https://monarch-initiative.github.io/monochrom/)|
|schema_url|[https://github.com/monarch-initiative/monochrom/blob/master/model/schema/chromo.yaml](https://github.com/monarch-initiative/monochrom/blob/master/model/schema/chromo.yaml)|
|github_repo|monarch-initiative/monochrom|
|license|CC-0|
|topics|genomics|

## 

None


|key|value|
| :---: | :---: |
|name|GSC MIxS|
|topics|genomics|

## A schema for describing translations and language profiles for ontologies

None


|key|value|
| :---: | :---: |
|name|Babelon|
|title|A schema for describing translations and language profiles for ontologies|
|homepage|[https://matentzn.github.io/babelon/](https://matentzn.github.io/babelon/)|
|github_repo|matentzn/babelon|
|license|CC-0|
|topics|ontologies|

## HOT-TermCI

Terminology Core Common Model


|key|value|
| :---: | :---: |
|name|HOT-TermCI|
|title|HOT-TermCI|
|homepage|[https://github.com/HOT-Ecosystem/TermCI-model](https://github.com/HOT-Ecosystem/TermCI-model)|
|github_repo|HOT-Ecosystem/TermCI-model|
|schema_relative_path|src/schema/tccm_schema.yaml|
|topics|clinical|
|class_count|4|
|slot_count|15|
|enum_count|0|
|type_count|19|
|proportion_elements_with_a_description|1.0|
|proportion_elements_mapped|0.86|

## Alliance of Genome Resources Persistent Schema

Alliance Persistent Schema


|key|value|
| :---: | :---: |
|name|Alliance of Genome Resource Persistent Schema|
|title|Alliance of Genome Resources Persistent Schema|
|github_repo|alliance-genome/agr_curation_schema|
|schema_relative_path|model/schema/allianceModel.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|genomics|
|class_count|285|
|slot_count|600|
|enum_count|21|
|type_count|20|
|proportion_elements_with_a_description|0.71|
|proportion_elements_mapped|0.04|

## 

None


|key|value|
| :---: | :---: |
|name|SESAR|
|topics|earth science|

## 

None


|key|value|
| :---: | :---: |
|name|OBOGraphs|
|github_repo|biodatamodels/obograph|
|topics|ontologies|

## Metadata schema for the German Human Genome-Phenome Archive (GHGA)

The submission centric metadata schema for the German Human Genome-Phenome Archive (GHGA).


|key|value|
| :---: | :---: |
|name|GHGA Metadata|
|title|Metadata schema for the German Human Genome-Phenome Archive (GHGA)|
|homepage|[https://ghga-de.github.io/ghga-metadata-schema/](https://ghga-de.github.io/ghga-metadata-schema/)|
|github_repo|ghga-de/ghga-metadata-schema|
|schema_relative_path|src/schema/submission.yaml|
|class_count|26|
|slot_count|112|
|enum_count|30|
|type_count|19|
|proportion_elements_with_a_description|0.98|
|proportion_elements_mapped|0.18|

## Minimal Information About a new Cell Type


This schema is CJM's attempt to translate Tiago's [minimal info doc](https://docs.google.com/document/d/1EVgs2Z5dpJs7cbuSBwWlg1xOWQEqMtbSKRGgdneXnU8/edit#) into a LinkML schema

The schema is fairly minimal and is in the form of a "checklist" style schema. It is a set of fields mostly associated with this class:

  * [CellType](CellType.md)

There are a set of examples here:

  * [tests/input](https://github.com/cmungall/mianct-schema/tree/main/tests/input)

Currently the examples are YAML, but the YAML is deliberately flat as this is a "checklist" schema, and we could have TSV/CSV/xlsx here

TODO:

  - include "packages" and "checklists"; e.g.
      - a neuron package would have the enum for morphologies constrained
      - a transcriptomics package would make it required to enter the set of marker genes
      - see [MIxS schema](https://cmungall.github.io/mixs-source/) for example of how this might work
  - document how this relates to dosdp/robot templates
  
When should one provide an entry for a cell type in a MIANCT sheet?

 - When there is a claim of a new cell class (type or state) that has not been described before
 - When new information is discovered for a previously cataloged type that might influence its cataloguing (i.e. description of the presence in a different species or in a new location)
 - When a cell type mentioned in the article has been described before, but is not yet catalogued on an authoritative source like the Cell Ontology.


|key|value|
| :---: | :---: |
|name|MIANCT|
|title|Minimal Information About a new Cell Type|
|homepage|[https://cmungall.github.io/mianct-schema/](https://cmungall.github.io/mianct-schema/)|
|github_repo|cmungall/mianct-schema|
|schema_relative_path|model/schema/mianct.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|samples; cell types|
|class_count|2|
|slot_count|11|
|enum_count|3|
|type_count|20|
|proportion_elements_with_a_description|0.69|
|proportion_elements_mapped|0.75|

## iSamples

None


|key|value|
| :---: | :---: |
|name|iSamples|
|title|iSamples|
|homepage|[https://github.com/isamplesorg/metadata](https://github.com/isamplesorg/metadata)|
|github_repo|isamplesorg/metadata|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|samples; metadata; earth science|

## SPARQLFun

SPARQL Templates


|key|value|
| :---: | :---: |
|name|sparqlfun|
|title|SPARQLFun|
|homepage|[https://github.com/linkml/sparqlfun](https://github.com/linkml/sparqlfun)|
|github_repo|linkml/sparqlfun|
|schema_relative_path|sparqlfun/schema/sparqlfun.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|sparql; templates|
|class_count|92|
|slot_count|61|
|enum_count|2|
|type_count|21|
|proportion_elements_with_a_description|0.33|
|proportion_elements_mapped|0.34|

## The INvestigation of Co-occurring conditions across the Lifespan to Understand Down syndromE (INCLUDE) data model

None


|key|value|
| :---: | :---: |
|name|INCLUDE|
|title|The INvestigation of Co-occurring conditions across the Lifespan to Understand Down syndromE (INCLUDE) data model|
|homepage|[https://github.com/include-dcc/include-linkml](https://github.com/include-dcc/include-linkml)|
|github_repo|include-dcc/include-linkml|
|license|CC-0|
|topics|Ontologies; Down syndrome; Clinical research|

