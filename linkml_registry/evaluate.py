from linkml_runtime.linkml_model.meta import SchemaDefinition, Element, ClassDefinition, \
    SlotDefinition, TypeDefinition, EnumDefinition
from linkml_runtime.loaders import yaml_loader
from linkml.utils.schemaloader import load_raw_schema
from linkml.generators.yamlgen import YAMLGenerator
from .github_utils import get_stars, clone_repo
from .registry import SchemaMetadata, SchemaRegistry
import logging

def evaluate(sr: SchemaRegistry, use_github_api=True, workdir: str = None):
    for s in sr.entries.values():
        evaluate_schema_metadata(s, use_github_api=use_github_api, workdir=workdir)

def evaluate_schema_metadata(sm: SchemaMetadata, use_github_api=True, workdir=None):
    if use_github_api:
        stars = get_stars(sm)
        sm.github_stars = stars
    if sm.schema_relative_path:
        try:
            dir = clone_repo(sm, workdir=workdir)
            print(f'Cloned to: {dir}')
            path = f'{dir}/{sm.schema_relative_path}'
            schema = load_schema(path)
            evaluate_schema(schema, sm)
        except Exception as e:
            logging.error(f'Exception: {e}')
            sm.errors.append(f'Error with obtaining schema for {sm.name}: {e}')

def load_schema(path: str) -> SchemaDefinition:
    #schema = load_raw_schema(path, merge_modules=True)
    gen = YAMLGenerator(path, mergeimports=True)
    yaml = gen.serialize()
    #print(f'YAML={yaml}')
    schema = gen.schema
    print(f'Parsed schema: {schema.name} type: {type(schema)} classes: {type(schema.classes)} = {len(schema.classes)}')
#    filter_schema(schema)
    return schema

def filter_schema(schema: SchemaDefinition):
    """
    trim internal imports from schema
    """
    # TODO: ask Harold how to do this
    #nu_classes = [x for x in schema.classes.values() if not exclude_element(x)]
    #schema.classes = nu_classes
    #schema.classes = [x for x in schema.classes.values() if not exclude_element(x)]
    #schema.slots = [x for x in schema.slots.values() if not exclude_element(x)]
    #schema.types = [x for x in schema.types.values() if not exclude_element(x)]
    #schema.enums = [x for x in schema.enums.values() if not exclude_element(x)]
    None

def exclude_element(x: Element) -> bool:
    """
    true if element should be excluded.

    Currently the only criteria is that this is an import of a 'builtin' linkml type
    """
    if x.from_schema and x.from_schema.startswith('https://w3id.org/linkml/'):
        return True
    else:
        return False

def evaluate_schema(schema: SchemaDefinition, sm: SchemaMetadata):
    name = schema.name
    print(f'Loaded schema: {name}')
    if schema.license:
        sm.license = schema.license
    if schema.description and schema.description != '':
        sm.description = schema.description
    if schema.title and schema.title != '':
        sm.title = schema.title
    sm.class_count = len(schema.classes.values())
    print(f'CC: {sm.class_count}')
    sm.slot_count = len(schema.slots.values())
    sm.enum_count = len(schema.enums.values())
    sm.type_count = len(schema.types.values())
    elements = list(schema.classes.values()) + list(schema.slots.values()) + \
               list(schema.types.values()) + list(schema.enums.values())
    elements_with_descriptions = [x for x in elements if x.description is not None and x.description != '']
    sm.proportion_elements_with_a_description = len(elements_with_descriptions) / len(elements)
    elements_mapped = [x for x in elements if _is_mapped(x)]
    sm.proportion_elements_mapped = len(elements_mapped) / len(elements)

def _is_mapped(x: Element) -> bool:
    if (x.exact_mappings and len(x.exact_mappings) > 0):
        return True
    # todo: check if class_uri is distinct from
    if isinstance(x, ClassDefinition):
        if x.class_uri:
            return True
    if isinstance(x, SlotDefinition):
        if x.slot_uri:
            return True
    if isinstance(x, TypeDefinition):
        return True
    if isinstance(x, EnumDefinition):
        if x.permissible_values and len(x.permissible_values) > 0:
            if len([v for v in x.permissible_values.values() if not v.meaning]) > 0:
                return False
            else:
                return True
    return False

