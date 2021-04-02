# Auto generated from registry.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-04-02 14:17
# Schema: linkml_registry
#
# id: https://w3id.org/linkml_registry
# description: linkml_registry
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml.utils.slot import Slot
from linkml.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml.utils.formatutils import camelcase, underscore, sfx
from linkml.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml.utils.curienamespace import CurieNamespace
from linkml_model.types import String

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
LINKML_REGISTRY = CurieNamespace('linkml_registry', 'https://w3id.org/linkml_registry')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = LINKML_REGISTRY


# Types
class HttpsIdentifier(String):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "https identifier"
    type_model_uri = LINKML_REGISTRY.HttpsIdentifier


# Class references



@dataclass
class SchemaInfo(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML_REGISTRY.SchemaInfo
    class_class_curie: ClassVar[str] = "linkml_registry:SchemaInfo"
    class_name: ClassVar[str] = "schema info"
    class_model_uri: ClassVar[URIRef] = LINKML_REGISTRY.SchemaInfo

    name: Optional[str] = None
    homepage: Optional[Union[str, HttpsIdentifier]] = None
    schema_url: Optional[Union[str, HttpsIdentifier]] = None
    license: Optional[Union[str, "LicenseEnum"]] = None
    description: Optional[str] = None
    domain: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.homepage is not None and not isinstance(self.homepage, HttpsIdentifier):
            self.homepage = HttpsIdentifier(self.homepage)

        if self.schema_url is not None and not isinstance(self.schema_url, HttpsIdentifier):
            self.schema_url = HttpsIdentifier(self.schema_url)

        if self.license is not None and not isinstance(self.license, LicenseEnum):
            self.license = LicenseEnum(self.license)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.domain is not None and not isinstance(self.domain, str):
            self.domain = str(self.domain)

        super().__post_init__(**kwargs)


# Enumerations
class LicenseEnum(EnumDefinitionImpl):

    _defn = EnumDefinition(
        name="LicenseEnum",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "CC-BY",
                PermissibleValue(text="CC-BY",
                                 description="CC-BY") )
        setattr(cls, "CC-0",
                PermissibleValue(text="CC-0",
                                 description="CC-0") )

# Slots
class slots:
    pass

slots.name = Slot(uri=LINKML_REGISTRY.name, name="name", curie=LINKML_REGISTRY.curie('name'),
                   model_uri=LINKML_REGISTRY.name, domain=None, range=Optional[str])

slots.homepage = Slot(uri=LINKML_REGISTRY.homepage, name="homepage", curie=LINKML_REGISTRY.curie('homepage'),
                   model_uri=LINKML_REGISTRY.homepage, domain=None, range=Optional[Union[str, HttpsIdentifier]])

slots.schema_url = Slot(uri=LINKML_REGISTRY.schema_url, name="schema url", curie=LINKML_REGISTRY.curie('schema_url'),
                   model_uri=LINKML_REGISTRY.schema_url, domain=None, range=Optional[Union[str, HttpsIdentifier]])

slots.license = Slot(uri=LINKML_REGISTRY.license, name="license", curie=LINKML_REGISTRY.curie('license'),
                   model_uri=LINKML_REGISTRY.license, domain=None, range=Optional[Union[str, "LicenseEnum"]])

slots.description = Slot(uri=LINKML_REGISTRY.description, name="description", curie=LINKML_REGISTRY.curie('description'),
                   model_uri=LINKML_REGISTRY.description, domain=None, range=Optional[str])

slots.domain = Slot(uri=LINKML_REGISTRY.domain, name="domain", curie=LINKML_REGISTRY.curie('domain'),
                   model_uri=LINKML_REGISTRY.domain, domain=None, range=Optional[str])
