# LinkML Registry Entries

## LinkML Schema Metamodel

A metamodel for defining linked open data schemas


|key|value|
| :---: | :---: |
|name|LinkML Model|
|title|LinkML Schema Metamodel|
|homepage|[https://linkml.github.io/linkml-model/docs/](https://linkml.github.io/linkml-model/docs/)|
|schema_url|[https://github.com/linkml/linkml-model/blob/main/model/schema/meta.yaml](https://github.com/linkml/linkml-model/blob/main/model/schema/meta.yaml)|
|github_repo|linkml/linkml-model|
|schema_relative_path|model/schema/meta.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|meta|
|class_count|19|
|slot_count|125|
|enum_count|1|
|type_count|14|
|github_stars|10|
|proportion_elements_with_a_description|0.91|
|proportion_elements_mapped|0.99|

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
|github_stars|1|

## NMDC Schema

Schema for National Microbiome Data Collaborative (NMDC). This schem is organized into 3 separate modules:
  
This schema is organized into distinct modules:
  
 * a set of core types for representing data values
 * the mixs schema (auto-translated from mixs excel)
 * annotation schema
 * the NMDC schema itself


|key|value|
| :---: | :---: |
|name|NMDC|
|title|NMDC Schema|
|homepage|[https://microbiomedata.github.io/nmdc-schema/](https://microbiomedata.github.io/nmdc-schema/)|
|github_repo|microbiomedata/nmdc-schema|
|schema_relative_path|src/schema/nmdc.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|environmental microbiology|
|class_count|48|
|slot_count|884|
|enum_count|1|
|type_count|18|
|github_stars|5|
|proportion_elements_with_a_description|0.86|
|proportion_elements_mapped|0.99|

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
|class_count|257|
|slot_count|608|
|enum_count|9|
|type_count|27|
|github_stars|68|
|proportion_elements_with_a_description|0.67|
|proportion_elements_mapped|0.99|

## Simple Standard Sharing Object Mappings

Datamodel for Simple Standard for Sharing Ontology Mappings (SSSOM)


|key|value|
| :---: | :---: |
|name|SSSOM|
|title|Simple Standard Sharing Object Mappings|
|homepage|[https://sssom-py.readthedocs.io/](https://sssom-py.readthedocs.io/)|
|github_repo|mapping-commons/sssom-py|
|schema_relative_path|schema/sssom.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|information|
|class_count|3|
|slot_count|49|
|enum_count|1|
|type_count|14|
|github_stars|10|
|proportion_elements_with_a_description|0.98|
|proportion_elements_mapped|0.98|

## Knowledge Graph Change Language

None


|key|value|
| :---: | :---: |
|name|KGCL|
|title|Knowledge Graph Change Language|
|homepage|[https://cmungall.github.io/knowledge-graph-change-language/](https://cmungall.github.io/knowledge-graph-change-language/)|
|github_repo|cmungall/knowledge-graph-change-language|
|schema_relative_path|src/schema/kgcl.yaml|
|license|CC-0|
|topics|knowledge graphs|
|github_stars|13|
|errors|Error with obtaining schema for KGCL: Conflicting URIs (https://w3id.org/kgcl/basics, https://w3id.org/kgcl/prov) for item: description|

## Knowledge Graph Visualization Configuration

A data model for describing configurations / stylesheets for visualzing graphs, and in particular Knowledge Graphs or Ontologies. These graphs are characterized by having meaningful edge labels, node categories, IDs or URIs on each element, as well as additional rich metadata on the nodes or edges.
An example of a use of this is https://github.com/cmungall/obographviz


|key|value|
| :---: | :---: |
|name|KGViz|
|title|Knowledge Graph Visualization Configuration|
|homepage|[https://berkeleybop.github.io/kgviz-model/](https://berkeleybop.github.io/kgviz-model/)|
|github_repo|berkeleybop/kgviz-model|
|schema_relative_path|model/schema/kgviz.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|visualization|
|class_count|16|
|slot_count|30|
|enum_count|3|
|type_count|16|
|github_stars|4|
|proportion_elements_with_a_description|0.53|
|proportion_elements_mapped|0.95|

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
issues for details

See the [github repo](https://github.com/cmungall/semantic-sql) for code to convert
from the linkml yaml into SQL DDL


|key|value|
| :---: | :---: |
|name|Semantic Sql|
|title|Semantic SQL|
|homepage|[https://cmungall.github.io/semantic-sql/](https://cmungall.github.io/semantic-sql/)|
|github_repo|cmungall/semantic-sql|
|schema_relative_path|src/schema/semsql.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|ontologies|
|class_count|98|
|slot_count|80|
|enum_count|0|
|type_count|16|
|github_stars|10|
|proportion_elements_with_a_description|0.58|
|proportion_elements_mapped|1.0|

## Chemistry Data Model

A data model for managing information about chemical entities, ranging from atoms through molecules to complex mixtures.
Aspects of this have been cribbed from various sources including CHEBI, SIO, Wikipedia/Wikidata, the NCATS Translator Chemical Working Group, but all mistakes are my own.
For full context/motivation see the [GitHub repo](https://github.com/cmungall/chem-schema).


|key|value|
| :---: | :---: |
|name|Chemistry Schema|
|title|Chemistry Data Model|
|homepage|[https://cmungall.github.io/chem-schema/](https://cmungall.github.io/chem-schema/)|
|github_repo|cmungall/chem-schema|
|schema_relative_path|src/schema/chem.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|chemistry|
|class_count|120|
|slot_count|266|
|enum_count|5|
|type_count|22|
|github_stars|7|
|proportion_elements_with_a_description|0.46|
|proportion_elements_mapped|0.99|

## CRDC-H Model

None


|key|value|
| :---: | :---: |
|name|CCDH|
|title|CRDC-H Model|
|homepage|[https://cancerdhc.github.io/ccdhmodel](https://cancerdhc.github.io/ccdhmodel)|
|github_repo|cancerdhc/ccdhmodel|
|schema_relative_path|src/schema/ccdhmodel.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|cancer|
|class_count|41|
|slot_count|333|
|enum_count|108|
|type_count|21|
|github_stars|10|
|proportion_elements_with_a_description|0.99|
|proportion_elements_mapped|0.78|

## common association file formats

Various association data models


|key|value|
| :---: | :---: |
|name|ontology-associations|
|title|common association file formats|
|homepage|[https://biodatamodels.github.io/ontology-associations/](https://biodatamodels.github.io/ontology-associations/)|
|github_repo|biodatamodels/ontology-associations|
|schema_relative_path|src/schema/all.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|genomics|
|class_count|33|
|slot_count|124|
|enum_count|18|
|type_count|25|
|github_stars|4|
|proportion_elements_with_a_description|0.31|
|proportion_elements_mapped|0.94|

## Genome Feature Format LinkML rendering

Playing around with GFF spec


|key|value|
| :---: | :---: |
|name|GFF3|
|title|Genome Feature Format LinkML rendering|
|homepage|[https://biodatamodels.github.io/gff-schema/](https://biodatamodels.github.io/gff-schema/)|
|github_repo|biodatamodels/gff-schema|
|schema_relative_path|src/schema/gff.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|genomics|
|class_count|8|
|slot_count|38|
|enum_count|3|
|type_count|16|
|github_stars|5|
|proportion_elements_with_a_description|0.56|
|proportion_elements_mapped|0.95|

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
|github_stars|8|

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
|github_stars|1|

## HOT-TermCI

Terminology Core Common Model


|key|value|
| :---: | :---: |
|name|HOT-TermCI|
|title|HOT-TermCI|
|homepage|[https://github.com/HOT-Ecosystem/TermCI-model](https://github.com/HOT-Ecosystem/TermCI-model)|
|github_repo|HOT-Ecosystem/TermCI-model|
|schema_relative_path|src/schema/tccm_schema.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|clinical|
|class_count|4|
|slot_count|16|
|enum_count|0|
|type_count|14|
|github_stars|3|
|proportion_elements_with_a_description|0.97|
|proportion_elements_mapped|1.0|

## Alliance of Genome Resources Persistent Schema

Alliance Persistent Schema


|key|value|
| :---: | :---: |
|name|Alliance of Genome Resource Persistent Schema|
|title|Alliance of Genome Resources Persistent Schema|
|github_repo|alliance-genome/agr_curation_schema|
|schema_relative_path|src/schema/alliance_schema.yaml|
|license|[https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/)|
|topics|genomics|
|github_stars|3|
|errors|Error with obtaining schema for Alliance of Genome Resource Persistent Schema: [Errno 2] No such file or directory: '/Users/cjm/repos/linkml-registry/tmp/agr_curation_schema/src/schema/alliance_schema.yaml'|

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
|github_stars|3|

## Metadata schema for the German Human Genome-Phenome Archive (GHGA)

None


|key|value|
| :---: | :---: |
|name|GHGC Metadata|
|title|Metadata schema for the German Human Genome-Phenome Archive (GHGA)|
|homepage|[https://ghga-de.github.io/ghga-metadata-schema/](https://ghga-de.github.io/ghga-metadata-schema/)|
|github_repo|ghga-de/ghga-metadata-schema|
|schema_relative_path|src/schema/ghgc.yaml|
|github_stars|3|
|errors|Error with obtaining schema for GHGC Metadata: [Errno 2] No such file or directory: '/Users/cjm/repos/linkml-registry/tmp/ghga-metadata-schema/src/schema/ghgc.yaml'|

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
|class_count|2|
|slot_count|11|
|enum_count|3|
|type_count|15|
|github_stars|3|
|proportion_elements_with_a_description|0.64|
|proportion_elements_mapped|0.93|

