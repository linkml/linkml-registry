#!/usr/bin/env python
import click
import yaml
import shutil
import re
import json
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def should_exclude_entry(entry, exclusion_rules):
    """
    Check if an entry should be excluded based on the exclusion rules.
    
    Args:
        entry (dict): The registry entry to check
        exclusion_rules (list): List of exclusion rule dictionaries
        
    Returns:
        tuple: (bool, str) - Whether to exclude and the reason if excluded
    """
    for rule in exclusion_rules:
        pattern = rule['pattern']
        case_sensitive = rule.get('case_sensitive', False)
        
        # Convert entry to string for simple checking across all fields
        entry_str = json.dumps(entry, ensure_ascii=False)
        
        # Perform the match based on case sensitivity setting
        if case_sensitive:
            if re.search(pattern, entry_str):
                return True, f"Matched rule: {rule['description']}"
        else:
            if re.search(pattern, entry_str, re.IGNORECASE):
                return True, f"Matched rule: {rule['description']}"
                
    return False, ""

@click.command()
@click.option('--registry-file', default='models.yaml', help='Path to LinkML registry YAML file.')
@click.option('--output-dir', default='docs', help='Output directory for markdown files.')
@click.option('--templates-dir', default='src/doc_templates', help='Directory containing Jinja2 templates.')
@click.option('--overview-template', default='overview.jinja2', help='Filename of overview template.')
@click.option('--detail-template', default='registry.jinja2', help='Filename of detail template.')
@click.option('--src-docs-dir', default='src/docs', help='Source docs directory containing the registry.md file.')
@click.option('--exclude-config', default=None, help='Path to exclusion rules JSON file. If not provided, default rules will be used.')
def generate_docs(registry_file, output_dir, templates_dir, overview_template, detail_template, src_docs_dir, exclude_config):
    """Generate markdown documentation from LinkML registry data."""
    # Setup default exclusion rules
    default_exclusion_rules = [
        {
            "pattern": "not a schema",
            "description": "Exclude entries containing 'not a schema'",
            "case_sensitive": False
        },
        {
            "pattern": "draft",
            "description": "Exclude entries marked as 'draft'",
            "case_sensitive": False
        },
        {
            "pattern": "not yet public",
            "description": "Exclude entries that are not yet public",
            "case_sensitive": False
        }
    ]
    
    # Load custom exclusion rules if provided
    exclusion_rules = default_exclusion_rules
    if exclude_config:
        try:
            with open(exclude_config, 'r') as f:
                exclusion_rules = json.load(f)
                print(f"Loaded {len(exclusion_rules)} exclusion rules from {exclude_config}")
        except Exception as e:
            print(f"Error loading exclusion rules from {exclude_config}: {e}")
            print(f"Using default exclusion rules instead.")
    
    # Setup Jinja environment
    env = Environment(loader=FileSystemLoader(templates_dir))

    # Load templates
    overview_tmpl = env.get_template(overview_template)
    detail_tmpl = env.get_template(detail_template)

    # Load registry data
    with open(registry_file, 'r') as f:
        registry_data = yaml.safe_load(f)

    # Extract entries from registry
    all_entries = registry_data.get('entries', {})
    
    # Filter entries based on exclusion rules
    filtered_entries = {}
    excluded_count = 0
    
    for id, entry in all_entries.items():
        should_exclude, reason = should_exclude_entry(entry, exclusion_rules)
        if should_exclude:
            excluded_count += 1
            print(f"Excluding entry '{id}': {reason}")
        else:
            filtered_entries[id] = entry
    
    print(f"Filtered out {excluded_count} entries, keeping {len(filtered_entries)} entries")
    
    # Create output directories
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    detail_path = output_path / 'details'
    
    # Remove existing detail directory and recreate it (clean regeneration)
    if detail_path.exists():
        print(f"Removing existing detail directory at {detail_path}")
        shutil.rmtree(detail_path)
    
    detail_path.mkdir(parents=True, exist_ok=True)

    # Generate overview content with filtered entries
    overview_content = overview_tmpl.render(entries=filtered_entries)

    # Update registry.md in both src/docs and output_dir
    src_registry_md = Path(src_docs_dir) / 'registry.md'
    if src_registry_md.exists():
        print(f"Overwriting existing registry file at {src_registry_md}")
        with open(src_registry_md, 'w') as f:
            f.write(overview_content)

    with open(output_path / 'registry.md', 'w') as f:
        f.write(overview_content)

    # Generate detail pages for each entry
    for id, entry in filtered_entries.items():
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
    print(f"- {len(filtered_entries)} detail pages in {detail_path}")

if __name__ == '__main__':
    generate_docs()