#!/usr/bin/env python
import click
import yaml
import shutil
from jinja2 import Environment, FileSystemLoader
from pathlib import Path


@click.command()
@click.option('--registry-file', default='models.yaml', help='Path to LinkML registry YAML file.')
@click.option('--output-dir', default='docs', help='Output directory for markdown files.')
@click.option('--templates-dir', default='src/doc_templates', help='Directory containing Jinja2 templates.')
@click.option('--overview-template', default='overview.jinja2', help='Filename of overview template.')
@click.option('--detail-template', default='registry.jinja2', help='Filename of detail template.')
@click.option('--src-docs-dir', default='src/docs', help='Source docs directory containing the registry.md file.')
def generate_docs(registry_file, output_dir, templates_dir, overview_template, detail_template, src_docs_dir):
    """Generate markdown documentation from LinkML registry data."""
    
    # Setup Jinja environment
    env = Environment(loader=FileSystemLoader(templates_dir))

    # Load templates
    overview_tmpl = env.get_template(overview_template)
    detail_tmpl = env.get_template(detail_template)

    # Load registry data
    with open(registry_file, 'r') as f:
        registry_data = yaml.safe_load(f)

    # Extract entries from registry
    entries = registry_data.get('entries', {})
    
    # Create output directories
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    detail_path = output_path / 'details'
    
    # Remove existing detail directory and recreate it (clean regeneration)
    if detail_path.exists():
        print(f"Removing existing detail directory at {detail_path}")
        shutil.rmtree(detail_path)
    
    detail_path.mkdir(parents=True, exist_ok=True)

    # Generate overview content
    overview_content = overview_tmpl.render(entries=entries)

    # Update registry.md in both src/docs and output_dir
    src_registry_md = Path(src_docs_dir) / 'registry.md'
    if src_registry_md.exists():
        print(f"Overwriting existing registry file at {src_registry_md}")
        with open(src_registry_md, 'w') as f:
            f.write(overview_content)

    with open(output_path / 'registry.md', 'w') as f:
        f.write(overview_content)

    # Generate detail pages for each entry
    for id, entry in entries.items():
        # Ensure entry has an id field for the template
        entry_with_id = dict(entry)
        entry_with_id['id'] = id

        detail_content = detail_tmpl.render(entry=entry_with_id)
        filename = id.replace(':', '_').replace('/', '_') + '.md'
        with open(detail_path / filename, 'w') as f:
            f.write(detail_content)

    # Copy other markdown files from src/docs to output_dir if they exist
    for md_file in Path(src_docs_dir).glob('*.md'):
        if md_file.name != 'registry.md':  # Skip registry.md as we've already handled it
            print(f"Copying {md_file} to {output_path / md_file.name}")
            shutil.copy2(md_file, output_path / md_file.name)

    print(f"Generated documentation in {output_path}")
    print(f"- Overview page: {output_path / 'registry.md'}")
    print(f"- {len(entries)} detail pages in {detail_path}")

if __name__ == '__main__':
    generate_docs()