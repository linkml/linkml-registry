"""
convenience wrappers around linkml runtime, for doing basic conversion between objects
and serialization formats.

The top level class is a Registry object

Some of this will become unnecessary in the future
"""
import yaml
import click
import logging
import os
import csv
from linkml_registry.registry import SchemaMetadata, SchemaRegistry
from typing import List


THIS_DIR = os.path.abspath(os.path.dirname(__file__))


def from_csv(filename: str, sep=',', name='default') -> SchemaRegistry:
    """
    Will be replaced by runtime csv method
    """
    logging.info(f'Converting {filename}')
    registry = SchemaRegistry(name=name)
    with open(filename, newline='') as tsvfile:
        rr = csv.DictReader(tsvfile, delimiter=sep)
        for row in rr:
            m = SchemaMetadata(**dict(row))
            registry.entries[m.name] = m
    return registry

@click.command()
@click.argument('files', nargs=-1)
def cli(files: List[str]):
    for f in files:
        registry = from_csv(f)

if __name__ == "__main__":
    cli()


