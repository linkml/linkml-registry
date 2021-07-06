import logging
import unittest
import os
from linkml_registry.registry import SchemaMetadata, SchemaRegistry
from linkml_registry.evaluate import evaluate
from linkml_registry.utils import from_csv
from linkml_registry.markdown_dumper import MarkdownTableDumper, MarkdownPageDumper
from linkml_runtime.dumpers import json_dumper, yaml_dumper
from linkml_runtime.loaders import yaml_loader

cwd = os.path.abspath(os.path.dirname(__file__))
EXAMPLE_DIR = os.path.join(cwd, 'inputs')
OUTPUT_DIR = os.path.join(cwd, 'outputs')
MARKDOWN_TABLE_OUTPUT = os.path.join(OUTPUT_DIR, 'registry.table.md')
MARKDOWN_OUTPUT = os.path.join(OUTPUT_DIR, 'registry.md')


class ConversionTestSuite(unittest.TestCase):
    """
    Reads examples from root /examples/ folder, converts them to json and rdf
    """

    def test_convert(self):
        #registry = from_csv(f'{EXAMPLE_DIR}/models.csv')
        registry = yaml_loader.load(os.path.join(EXAMPLE_DIR, 'test_models.yaml'), SchemaRegistry)
        ofn = os.path.join(OUTPUT_DIR, "test.yaml")
        with open(ofn, "w") as stream:
            stream.write(yaml_dumper.dumps(registry))
        evaluate(registry, use_github_api=False)
        print(f'R: {registry}')
        json = json_dumper.dumps(registry)
        ofn = os.path.join(OUTPUT_DIR, "test.json")
        with open(ofn, "w") as stream:
            stream.write(json)
        d = MarkdownTableDumper()
        d.dump(registry, to_file=MARKDOWN_TABLE_OUTPUT)
        d = MarkdownPageDumper()
        d.dump(registry, to_file=MARKDOWN_OUTPUT)
        #with open(os.path.join(OUTPUT_DIR, "test.jsonld"), "w") as stream:
        #    stream.write(to_jsonld(session))
        #G: Graph
        #G = to_rdf(session)
        #G.serialize(os.path.join(OUTPUT_DIR, "test.rdf"), format='turtle')

