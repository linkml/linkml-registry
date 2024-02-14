
from dataclasses import dataclass
from dataclasses import field
from typing import List

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import Integer
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

mapper_registry = registry()
metadata = MetaData()

from linkml_registry import *


tbl_schema_metadata = Table('schema_metadata', metadata, 
    Column('name', Text, primary_key=True),
    Column('title', Text),
    Column('description', Text),
    Column('homepage', Text),
    Column('schema_url', Text),
    Column('github_repo', Text),
    Column('schema_relative_path', Text),
    Column('license', Text),
    Column('score', Text),
    Column('class_count', Text),
    Column('slot_count', Text),
    Column('enum_count', Text),
    Column('type_count', Text),
    Column('github_stars', Text),
    Column('proportion_elements_with_a_description', Text),
    Column('proportion_elements_mapped', Text),
    Column('schema_registry_name', Text, ForeignKey('schema_registry.name')),
)
tbl_schema_registry = Table('schema_registry', metadata, 
    Column('name', Text, primary_key=True),
    Column('homepage', Text),
    Column('license', Text),
    Column('title', Text),
    Column('description', Text),
)
tbl_schema_metadata_domain = Table('schema_metadata_domain', metadata, 
    Column('backref_id', Text, ForeignKey('schema_metadata.name'), primary_key=True),
    Column('domain', Text, primary_key=True),
)
tbl_schema_metadata_topics = Table('schema_metadata_topics', metadata, 
    Column('backref_id', Text, ForeignKey('schema_metadata.name'), primary_key=True),
    Column('topics', Text, primary_key=True),
)
tbl_schema_metadata_errors = Table('schema_metadata_errors', metadata, 
    Column('backref_id', Text, ForeignKey('schema_metadata.name'), primary_key=True),
    Column('errors', Text, primary_key=True),
)
tbl_schema_registry_domain = Table('schema_registry_domain', metadata, 
    Column('backref_id', Text, ForeignKey('schema_registry.name'), primary_key=True),
    Column('domain', Text, primary_key=True),
)
tbl_schema_registry_topics = Table('schema_registry_topics', metadata, 
    Column('backref_id', Text, ForeignKey('schema_registry.name'), primary_key=True),
    Column('topics', Text, primary_key=True),
)
mapper_registry.map_imperatively(SchemaMetadata, tbl_schema_metadata, properties={
})
mapper_registry.map_imperatively(SchemaRegistry, tbl_schema_registry, properties={

    'entries': 
        relationship(schema metadata, 
                      foreign_keys=tbl_schema_metadata.columns["schema_registry_name"],
                      backref='SchemaRegistry'),

})
