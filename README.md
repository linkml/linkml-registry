# LinkML Registry

An automatically generated registry of LinkML schemas discovered from GitHub repositories.

## View the Registry

* **Documentation**: [https://linkml.github.io/linkml-registry/registry/](https://linkml.github.io/linkml-registry/registry/)
* **Registry Data**: [linkml_registry.yaml](linkml_registry.yaml)

## Registry Generation

The LinkML Registry is automatically generated using GitHub's Search API to discover repositories that use LinkML. 
The registry is updated through automated scripts that search for, analyze, and catalog LinkML projects.

### Discovery Script

The main discovery script (`src/scripts/discover_linkml_repos.py`) performs the following operations:

#### Search Queries
- **Repository searches**: Queries for repositories containing "linkml", "linkml-project-cookiecutter", 
"linkml in:description", and "LinkML in:description"
- **File content searches**: Searches for "linkml" in specific files including:
  - `pyproject.toml`
  - `requirements.txt`
  - `setup.py`, `setup.cfg`
  - `poetry.lock`, `Pipfile`
  - README files (`.md`, `.rst`)

**Note**: GitHub's code search API does not index all repositories or files immediately. Some repositories, particularly newer ones or those with lower activity, may not have their files indexed and therefore won't be discovered through file content searches. If your LinkML project is not appearing in the registry, it may be due to GitHub's indexing limitations rather than the search criteria.

#### Filtering Logic
The following filters are applied to discovered repositories:

- **Fork exclusion**: Skips forked repositories to focus on original projects
- **LinkML organization exclusion**: Excludes repositories from the `linkml/` organization itself to focus on external usage
- **Minimum stars**: Configurable minimum GitHub star count (default: 0)
- **Archive status**: Filters out archived repositories during analysis

#### Repository Analysis
For each discovered repository, the script extracts:

- **Basic metadata**: Title, description, license, GitHub URL
- **Domain classification**: Categorizes projects by domain (Biology, Computer Science, Chemistry, etc.)
- **Status determination**: Assesses if projects are active, inactive, or maintenance mode
- **Topics extraction**: Collects relevant GitHub topics, filtering out generic ones
- **Schema URL detection**: Attempts to identify documentation URLs (GitHub Pages, w3id.org)
- **Contact information**: Extracts repository owner/organization

#### Sorting and Organization
- **Primary sort**: By GitHub star count (descending)
- **Secondary sort**: Alphabetically by repository title within same star count

### Regeneration Schedule

The registry is automatically updated through GitHub Actions workflows:

- **Trigger**: Push to main branch or manual dispatch
- **Frequency**: Can be run on-demand via the GitHub Actions interface
- **Process**: 
  1. Runs discovery script to update `linkml_registry.yaml`
  2. Generates documentation from the updated registry
  3. Commits changes back to the repository
  4. Deploys updated documentation to GitHub Pages

### Manual Generation

To manually update the registry:

```bash
# Discover and update the registry
make discover

# Generate documentation
make gendoc

# View locally
make testdoc
```

### Scripts and Configuration

- **Discovery script**: `src/scripts/discover_linkml_repos.py`
- **Documentation generator**: `src/scripts/generate_registry_docs.py`
- **Template files**: `src/doc_templates/`
- **Makefile targets**: `discover`, `gendoc`, `testdoc`

### GitHub Workflows

- **`.github/workflows/regenerate-registry.yaml`**: Updates registry data
- **`.github/workflows/deploy-docs.yaml`**: Deploys documentation to GitHub Pages
- **`.github/workflows/test-pr.yaml`**: Runs tests on pull requests

The registry serves as a comprehensive catalog of the LinkML ecosystem, helping users discover projects, tools, 
and schemas that utilize the LinkML framework.