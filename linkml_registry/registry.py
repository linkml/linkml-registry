# Auto generated from registry.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-07-05 17:10
# Schema: linkml_registry
#
# id: https://w3id.org/linkml_registry
# description: Datamodel for LinkML Registry and evaluation framework
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Float, Integer, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
OIO = CurieNamespace('OIO', 'http://www.geneontology.org/formats/oboInOwl#')
BIBO = CurieNamespace('bibo', 'http://purl.org/ontology/bibo/')
DCAT = CurieNamespace('dcat', 'http://www.w3.org/ns/dcat#')
DCTERMS = CurieNamespace('dcterms', 'http://example.org/UNKNOWN/dcterms/')
DOAP = CurieNamespace('doap', 'http://usefulinc.com/ns/doap#')
FOAF = CurieNamespace('foaf', 'http://xmlns.com/foaf/0.1/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
LINKML_REGISTRY = CurieNamespace('linkml_registry', 'https://w3id.org/linkml_registry')
OSLC = CurieNamespace('oslc', 'http://open-services.net/ns/core#')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
RDFS = CurieNamespace('rdfs', 'http://example.org/UNKNOWN/rdfs/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = LINKML_REGISTRY


# Types
class HttpsIdentifier(String):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "https identifier"
    type_model_uri = LINKML_REGISTRY.HttpsIdentifier


# Class references
class SchemaRegistryName(extended_str):
    pass


class SchemaMetadataName(extended_str):
    pass


@dataclass
class SchemaRegistry(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML_REGISTRY.SchemaRegistry
    class_class_curie: ClassVar[str] = "linkml_registry:SchemaRegistry"
    class_name: ClassVar[str] = "schema registry"
    class_model_uri: ClassVar[URIRef] = LINKML_REGISTRY.SchemaRegistry

    name: Union[str, SchemaRegistryName] = None
    homepage: Optional[Union[str, HttpsIdentifier]] = None
    entries: Optional[Union[Dict[Union[str, SchemaMetadataName], Union[dict, "SchemaMetadata"]], List[Union[dict, "SchemaMetadata"]]]] = empty_dict()
    license: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    domain: Optional[Union[str, List[str]]] = empty_list()
    topics: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SchemaRegistryName):
            self.name = SchemaRegistryName(self.name)

        if self.homepage is not None and not isinstance(self.homepage, HttpsIdentifier):
            self.homepage = HttpsIdentifier(self.homepage)

        self._normalize_inlined_as_dict(slot_name="entries", slot_type=SchemaMetadata, key_name="name", keyed=True)

        if self.license is not None and not isinstance(self.license, str):
            self.license = str(self.license)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.domain, list):
            self.domain = [self.domain] if self.domain is not None else []
        self.domain = [v if isinstance(v, str) else str(v) for v in self.domain]

        if not isinstance(self.topics, list):
            self.topics = [self.topics] if self.topics is not None else []
        self.topics = [v if isinstance(v, str) else str(v) for v in self.topics]

        super().__post_init__(**kwargs)


@dataclass
class SchemaMetadata(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML_REGISTRY.SchemaMetadata
    class_class_curie: ClassVar[str] = "linkml_registry:SchemaMetadata"
    class_name: ClassVar[str] = "schema metadata"
    class_model_uri: ClassVar[URIRef] = LINKML_REGISTRY.SchemaMetadata

    name: Union[str, SchemaMetadataName] = None
    title: Optional[str] = None
    description: Optional[str] = None
    homepage: Optional[Union[str, HttpsIdentifier]] = None
    schema_url: Optional[Union[str, HttpsIdentifier]] = None
    github_repo: Optional[str] = None
    schema_relative_path: Optional[str] = None
    license: Optional[str] = None
    domain: Optional[Union[str, List[str]]] = empty_list()
    topics: Optional[Union[str, List[str]]] = empty_list()
    score: Optional[str] = None
    class_count: Optional[int] = None
    slot_count: Optional[int] = None
    enum_count: Optional[int] = None
    type_count: Optional[int] = None
    github_stars: Optional[int] = None
    proportion_elements_with_a_description: Optional[float] = None
    proportion_elements_mapped: Optional[float] = None
    errors: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SchemaMetadataName):
            self.name = SchemaMetadataName(self.name)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.homepage is not None and not isinstance(self.homepage, HttpsIdentifier):
            self.homepage = HttpsIdentifier(self.homepage)

        if self.schema_url is not None and not isinstance(self.schema_url, HttpsIdentifier):
            self.schema_url = HttpsIdentifier(self.schema_url)

        if self.github_repo is not None and not isinstance(self.github_repo, str):
            self.github_repo = str(self.github_repo)

        if self.schema_relative_path is not None and not isinstance(self.schema_relative_path, str):
            self.schema_relative_path = str(self.schema_relative_path)

        if self.license is not None and not isinstance(self.license, str):
            self.license = str(self.license)

        if not isinstance(self.domain, list):
            self.domain = [self.domain] if self.domain is not None else []
        self.domain = [v if isinstance(v, str) else str(v) for v in self.domain]

        if not isinstance(self.topics, list):
            self.topics = [self.topics] if self.topics is not None else []
        self.topics = [v if isinstance(v, str) else str(v) for v in self.topics]

        if self.score is not None and not isinstance(self.score, str):
            self.score = str(self.score)

        if self.class_count is not None and not isinstance(self.class_count, int):
            self.class_count = int(self.class_count)

        if self.slot_count is not None and not isinstance(self.slot_count, int):
            self.slot_count = int(self.slot_count)

        if self.enum_count is not None and not isinstance(self.enum_count, int):
            self.enum_count = int(self.enum_count)

        if self.type_count is not None and not isinstance(self.type_count, int):
            self.type_count = int(self.type_count)

        if self.github_stars is not None and not isinstance(self.github_stars, int):
            self.github_stars = int(self.github_stars)

        if self.proportion_elements_with_a_description is not None and not isinstance(self.proportion_elements_with_a_description, float):
            self.proportion_elements_with_a_description = float(self.proportion_elements_with_a_description)

        if self.proportion_elements_mapped is not None and not isinstance(self.proportion_elements_mapped, float):
            self.proportion_elements_mapped = float(self.proportion_elements_mapped)

        if not isinstance(self.errors, list):
            self.errors = [self.errors] if self.errors is not None else []
        self.errors = [v if isinstance(v, str) else str(v) for v in self.errors]

        super().__post_init__(**kwargs)


@dataclass
class Evaluation(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML_REGISTRY.Evaluation
    class_class_curie: ClassVar[str] = "linkml_registry:Evaluation"
    class_name: ClassVar[str] = "evaluation"
    class_model_uri: ClassVar[URIRef] = LINKML_REGISTRY.Evaluation

    score: Optional[str] = None
    class_count: Optional[int] = None
    slot_count: Optional[int] = None
    enum_count: Optional[int] = None
    type_count: Optional[int] = None
    github_stars: Optional[int] = None
    proportion_elements_with_a_description: Optional[float] = None
    proportion_elements_mapped: Optional[float] = None
    errors: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.score is not None and not isinstance(self.score, str):
            self.score = str(self.score)

        if self.class_count is not None and not isinstance(self.class_count, int):
            self.class_count = int(self.class_count)

        if self.slot_count is not None and not isinstance(self.slot_count, int):
            self.slot_count = int(self.slot_count)

        if self.enum_count is not None and not isinstance(self.enum_count, int):
            self.enum_count = int(self.enum_count)

        if self.type_count is not None and not isinstance(self.type_count, int):
            self.type_count = int(self.type_count)

        if self.github_stars is not None and not isinstance(self.github_stars, int):
            self.github_stars = int(self.github_stars)

        if self.proportion_elements_with_a_description is not None and not isinstance(self.proportion_elements_with_a_description, float):
            self.proportion_elements_with_a_description = float(self.proportion_elements_with_a_description)

        if self.proportion_elements_mapped is not None and not isinstance(self.proportion_elements_mapped, float):
            self.proportion_elements_mapped = float(self.proportion_elements_mapped)

        if not isinstance(self.errors, list):
            self.errors = [self.errors] if self.errors is not None else []
        self.errors = [v if isinstance(v, str) else str(v) for v in self.errors]

        super().__post_init__(**kwargs)


# Enumerations
class LicenseEnum(EnumDefinitionImpl):

    _defn = EnumDefinition(
        name="LicenseEnum",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "CC-BY-v4",
                PermissibleValue(text="CC-BY-v4",
                                 description="CC-BY",
                                 meaning=None) )
        setattr(cls, "CC-0-v1",
                PermissibleValue(text="CC-0-v1",
                                 description="CC-0",
                                 meaning=None) )

# Slots
class slots:
    pass

slots.name = Slot(uri=RDFS.label, name="name", curie=RDFS.curie('label'),
                   model_uri=LINKML_REGISTRY.name, domain=None, range=URIRef)

slots.base_purl = Slot(uri=LINKML_REGISTRY.base_purl, name="base purl", curie=LINKML_REGISTRY.curie('base_purl'),
                   model_uri=LINKML_REGISTRY.base_purl, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.schema_purl = Slot(uri=LINKML_REGISTRY.schema_purl, name="schema purl", curie=LINKML_REGISTRY.curie('schema_purl'),
                   model_uri=LINKML_REGISTRY.schema_purl, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.homepage = Slot(uri=FOAF.homepage, name="homepage", curie=FOAF.curie('homepage'),
                   model_uri=LINKML_REGISTRY.homepage, domain=None, range=Optional[Union[str, HttpsIdentifier]])

slots.schema_url = Slot(uri=DCTERMS.source, name="schema url", curie=DCTERMS.curie('source'),
                   model_uri=LINKML_REGISTRY.schema_url, domain=None, range=Optional[Union[str, HttpsIdentifier]])

slots.github_repo = Slot(uri=LINKML_REGISTRY.github_repo, name="github repo", curie=LINKML_REGISTRY.curie('github_repo'),
                   model_uri=LINKML_REGISTRY.github_repo, domain=None, range=Optional[str])

slots.issue_tracker = Slot(uri=DOAP['bug-database'], name="issue tracker", curie=DOAP.curie('bug-database'),
                   model_uri=LINKML_REGISTRY.issue_tracker, domain=None, range=Optional[str])

slots.license = Slot(uri=DCTERMS.license, name="license", curie=DCTERMS.curie('license'),
                   model_uri=LINKML_REGISTRY.license, domain=None, range=Optional[str])

slots.title = Slot(uri=DCTERMS.title, name="title", curie=DCTERMS.curie('title'),
                   model_uri=LINKML_REGISTRY.title, domain=None, range=Optional[str])

slots.description = Slot(uri=SKOS.definition, name="description", curie=SKOS.curie('definition'),
                   model_uri=LINKML_REGISTRY.description, domain=None, range=Optional[str])

slots.domain = Slot(uri=DCTERMS.subject, name="domain", curie=DCTERMS.curie('subject'),
                   model_uri=LINKML_REGISTRY.domain, domain=None, range=Optional[Union[str, List[str]]])

slots.topics = Slot(uri=DCTERMS.subject, name="topics", curie=DCTERMS.curie('subject'),
                   model_uri=LINKML_REGISTRY.topics, domain=None, range=Optional[Union[str, List[str]]])

slots.entries = Slot(uri=DCTERMS.hasPart, name="entries", curie=DCTERMS.curie('hasPart'),
                   model_uri=LINKML_REGISTRY.entries, domain=None, range=Optional[Union[Dict[Union[str, SchemaMetadataName], Union[dict, SchemaMetadata]], List[Union[dict, SchemaMetadata]]]])

slots.score = Slot(uri=LINKML_REGISTRY.score, name="score", curie=LINKML_REGISTRY.curie('score'),
                   model_uri=LINKML_REGISTRY.score, domain=None, range=Optional[int])

slots.github_stars = Slot(uri=LINKML_REGISTRY.github_stars, name="github stars", curie=LINKML_REGISTRY.curie('github_stars'),
                   model_uri=LINKML_REGISTRY.github_stars, domain=None, range=Optional[int])

slots.schema_relative_path = Slot(uri=LINKML_REGISTRY.schema_relative_path, name="schema relative path", curie=LINKML_REGISTRY.curie('schema_relative_path'),
                   model_uri=LINKML_REGISTRY.schema_relative_path, domain=None, range=Optional[str])

slots.statistic = Slot(uri=LINKML_REGISTRY.statistic, name="statistic", curie=LINKML_REGISTRY.curie('statistic'),
                   model_uri=LINKML_REGISTRY.statistic, domain=None, range=Optional[str])

slots.count_statistic = Slot(uri=LINKML_REGISTRY.count_statistic, name="count statistic", curie=LINKML_REGISTRY.curie('count_statistic'),
                   model_uri=LINKML_REGISTRY.count_statistic, domain=None, range=Optional[int])

slots.proportion_statistic = Slot(uri=LINKML_REGISTRY.proportion_statistic, name="proportion statistic", curie=LINKML_REGISTRY.curie('proportion_statistic'),
                   model_uri=LINKML_REGISTRY.proportion_statistic, domain=None, range=Optional[float])

slots.evaluation__score = Slot(uri=LINKML_REGISTRY.score, name="evaluation__score", curie=LINKML_REGISTRY.curie('score'),
                   model_uri=LINKML_REGISTRY.evaluation__score, domain=None, range=Optional[str])

slots.evaluation__class_count = Slot(uri=LINKML_REGISTRY.class_count, name="evaluation__class_count", curie=LINKML_REGISTRY.curie('class_count'),
                   model_uri=LINKML_REGISTRY.evaluation__class_count, domain=None, range=Optional[int])

slots.evaluation__slot_count = Slot(uri=LINKML_REGISTRY.slot_count, name="evaluation__slot_count", curie=LINKML_REGISTRY.curie('slot_count'),
                   model_uri=LINKML_REGISTRY.evaluation__slot_count, domain=None, range=Optional[int])

slots.evaluation__enum_count = Slot(uri=LINKML_REGISTRY.enum_count, name="evaluation__enum_count", curie=LINKML_REGISTRY.curie('enum_count'),
                   model_uri=LINKML_REGISTRY.evaluation__enum_count, domain=None, range=Optional[int])

slots.evaluation__type_count = Slot(uri=LINKML_REGISTRY.type_count, name="evaluation__type_count", curie=LINKML_REGISTRY.curie('type_count'),
                   model_uri=LINKML_REGISTRY.evaluation__type_count, domain=None, range=Optional[int])

slots.evaluation__github_stars = Slot(uri=LINKML_REGISTRY.github_stars, name="evaluation__github_stars", curie=LINKML_REGISTRY.curie('github_stars'),
                   model_uri=LINKML_REGISTRY.evaluation__github_stars, domain=None, range=Optional[int])

slots.evaluation__proportion_elements_with_a_description = Slot(uri=LINKML_REGISTRY.proportion_elements_with_a_description, name="evaluation__proportion_elements_with_a_description", curie=LINKML_REGISTRY.curie('proportion_elements_with_a_description'),
                   model_uri=LINKML_REGISTRY.evaluation__proportion_elements_with_a_description, domain=None, range=Optional[float])

slots.evaluation__proportion_elements_mapped = Slot(uri=LINKML_REGISTRY.proportion_elements_mapped, name="evaluation__proportion_elements_mapped", curie=LINKML_REGISTRY.curie('proportion_elements_mapped'),
                   model_uri=LINKML_REGISTRY.evaluation__proportion_elements_mapped, domain=None, range=Optional[float])

slots.evaluation__errors = Slot(uri=LINKML_REGISTRY.errors, name="evaluation__errors", curie=LINKML_REGISTRY.curie('errors'),
                   model_uri=LINKML_REGISTRY.evaluation__errors, domain=None, range=Optional[Union[str, List[str]]])
