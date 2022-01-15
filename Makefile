# All artifacts of the build should be preserved
.SECONDARY:

# ----------------------------------------
# Model documentation and schema directory
# ----------------------------------------
SRC_DIR = src
PKG_DIR = linkml_registry
SCHEMA_DIR = $(SRC_DIR)/schema
MODEL_DOCS_DIR = $(SRC_DIR)/docs
SOURCE_FILES := $(shell find $(SCHEMA_DIR) -name '*.yaml')
SRC = $(SCHEMA_DIR)/registry.yaml
SCHEMA_NAMES = $(patsubst $(SCHEMA_DIR)/%.yaml, %, $(SOURCE_FILES))

SCHEMA_NAME = registry
SCHEMA_SRC = $(SCHEMA_DIR)/$(SCHEMA_NAME).yaml
PKG_TGTS = python jsonld_context json_schema
TGTS = docs python $(PKG_TGTS)

# Targets by PKG_TGT
PKG_T_GRAPHQL = $(PKG_DIR)/graphql
PKG_T_JSON = $(PKG_DIR)/json
PKG_T_JSONLD_CONTEXT = $(PKG_DIR)/jsonld
PKG_T_JSON_SCHEMA = $(PKG_DIR)/jsonschema
PKG_T_OWL = $(PKG_DIR)/owl
PKG_T_RDF = $(PKG_DIR)/rdf
PKG_T_SHEX = $(PKG_DIR)/shex
PKG_T_SQLDDL = $(PKG_DIR)/sqlddl
PKG_T_DOCS = $(MODEL_DOCS_DIR)
PKG_T_PYTHON = $(PKG_DIR)
PKG_T_MODEL = $(PKG_DIR)/model
PKG_T_SCHEMA = $(PKG_T_MODEL)/schema

# Global generation options
GEN_OPTS = --log_level WARNING
ENV = export PIPENV_VENV_IN_PROJECT=true && export PIPENV_PIPFILE=make-venv/Pipfile && export PIPENV_IGNORE_VIRTUALENVS=1
RUN = pipenv run

# ----------------------------------------
# TOP LEVEL TARGETS
# ----------------------------------------
all: install gen
index: models.yaml all

# ---------------------------------------
# We don't want to pollute the python environment with linkml tool specific packages.  For this reason,
# we install an isolated instance of linkml in the pipenv-linkml directory
# ---------------------------------------
install: make-venv/env.lock

make-venv/env.lock:
	$(ENV) && pipenv install
	touch make-venv/env.lock

uninstall:
	rm -f make-venv/env.lock
	$(ENV) && pipenv --rm

# ---------------------------------------
# Test runner
# ----------------------------------------
test:
	pipenv install --dev
	pipenv run python -m unittest discover -p 'test_*.py'

# ---------------------------------------
# GEN: run generator for each target
# ---------------------------------------
#gen: $(patsubst %,gen-%,$(TGTS))

gen:
	$(RUN) gen-project -d . $(SRC)

markdown:
	$(RUN) gen-markdown -d target/docs/ -I index.md $(SRC)  && \
	cp src/docs/*.md target/docs/

linkml_registry/registry.py: registry.py 
	cp $< $@



# test docs locally.
docserve:
	$(RUN) mkdocs serve
gh-deploy:
	$(RUN) mkdocs gh-deploy

models.yaml src/docs/registry.md: src/data/models.yaml
	pipenv run python -m linkml_registry.cli eval -i $< --use-github-api -m src/docs/registry.md -o models.yaml
