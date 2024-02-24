

CREATE TABLE schema_registry (
	name TEXT NOT NULL, 
	homepage TEXT, 
	license TEXT, 
	title TEXT, 
	description TEXT, 
	PRIMARY KEY (name)
);

CREATE TABLE schema_metadata (
	name TEXT NOT NULL, 
	title TEXT, 
	description TEXT, 
	homepage TEXT, 
	schema_url TEXT, 
	github_repo TEXT, 
	schema_relative_path TEXT, 
	license TEXT, 
	score TEXT, 
	class_count INTEGER, 
	slot_count INTEGER, 
	enum_count INTEGER, 
	type_count INTEGER, 
	github_stars INTEGER, 
	proportion_elements_with_a_description FLOAT, 
	proportion_elements_mapped FLOAT, 
	schema_registry_name TEXT, 
	PRIMARY KEY (name), 
	FOREIGN KEY(schema_registry_name) REFERENCES schema_registry (name)
);

CREATE TABLE schema_registry_domain (
	backref_id TEXT, 
	domain TEXT, 
	PRIMARY KEY (backref_id, domain), 
	FOREIGN KEY(backref_id) REFERENCES schema_registry (name)
);

CREATE TABLE schema_registry_topics (
	backref_id TEXT, 
	topics TEXT, 
	PRIMARY KEY (backref_id, topics), 
	FOREIGN KEY(backref_id) REFERENCES schema_registry (name)
);

CREATE TABLE schema_metadata_domain (
	backref_id TEXT, 
	domain TEXT, 
	PRIMARY KEY (backref_id, domain), 
	FOREIGN KEY(backref_id) REFERENCES schema_metadata (name)
);

CREATE TABLE schema_metadata_topics (
	backref_id TEXT, 
	topics TEXT, 
	PRIMARY KEY (backref_id, topics), 
	FOREIGN KEY(backref_id) REFERENCES schema_metadata (name)
);

CREATE TABLE schema_metadata_errors (
	backref_id TEXT, 
	errors TEXT, 
	PRIMARY KEY (backref_id, errors), 
	FOREIGN KEY(backref_id) REFERENCES schema_metadata (name)
);

