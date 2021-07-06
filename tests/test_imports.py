import unittest
from linkml_registry.registry import SchemaMetadata, SchemaRegistry

class ConversionTestSuite(unittest.TestCase):

    def test_import(self):
        r = SchemaRegistry(name='test')
