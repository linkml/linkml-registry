# LinkML Registry

The LinkML Registry is an automatically generated catalog of LinkML schemas, built by using GitHub’s Search API to discover repositories that reference LinkML.
It is maintained by automated scripts that continuously search for, analyze, and index LinkML-based projects.

* **Registry Data (YAML)**: [linkml_registry.yaml](linkml_registry.yaml)
* **Registry (Markdown)**: [https://linkml.github.io/linkml-registry/registry/](https://linkml.github.io/linkml-registry/registry/)

#### Howto Be Added to the Registry

Because the LinkML Registry is automatically generated, there is no manual submission process, however, you can ensure 
your project is included by follows the guidelines below:

- **Use LinkML**: Your project is in GitHub, uses `linkml` or one of its repos in its dependencies.
- **File content searches**: The current algorithm searches for "linkml" in project-specific configuration files including:
  - `pyproject.toml`
  - `requirements.txt`
  - `setup.py`, `setup.cfg`
  - `poetry.lock`, `Pipfile`
  - README files (`.md`, `.rst`)
- **Public Repository**: Ensure your repository is public and not archived and not forked from another project.
- **Bonus Repository Metadata**: Include relevant metadata in your repository:
  - A clear description of the project
  - Use of LinkML in your codebase
  - Relevant GitHub topics (e.g., `linkml`, `schema`, `ontology`)
  - License information

For more details on how LinkML schema projects are discovered, please see `src/scripts/discover_linkml_repos.py`.

#### Registry Sorting and Organization
- **Primary sort**: By GitHub star count (descending)
- **Secondary sort**: Alphabetically by repository title

### Regeneration Schedule

The registry is automatically updated through GitHub Actions workflows:

- **Trigger**: Push to main branch or manual dispatch
- **Frequency**: Can be run on-demand via the GitHub Actions interface
- **Process**: 
  1. Runs discovery script to update `linkml_registry.yaml`
  2. Generates documentation from the updated registry
  3. Commits changes back to the repository
  4. Deploys updated documentation to GitHub Pages


