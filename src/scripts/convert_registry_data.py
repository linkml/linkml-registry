#!/usr/bin/env python3
"""
Convert registry data from tabular format into models.yaml format.

This script converts data from a tab-separated spreadsheet format into the
YAML format used by the LinkML registry.
"""

import yaml
import sys
from typing import Dict, List, Any, Optional
import re

# Define the field mappings from spreadsheet columns to models.yaml structure
FIELD_MAPPINGS = {
    "org/repo": "name",
    "Schema": "title",
    "Schema URI": "uri",
    "Source URL (GitHub Preferred)": "schema_url",
    "Primary Technical Contacts": "contacts",
    "Type": "schema_type",
    "Domain": "domain",
    "Status": "status",
    "Description": "description",
    "Community Presentation": "community_presentation",
    "Community Members?": "has_community",
    "Derived_From": "derived_from",
    "Publications": "publications",
    "Funding": "funding",
    "Share metadata": "share_metadata",
    "Notes": "notes",
    "GitHub": "github_repo"
}

# Process the input data
def convert_data(input_text: str) -> Dict[str, Any]:
    """
    Convert the tab-separated input data to models.yaml format.
    
    Args:
        input_text: String containing tab-separated data
    
    Returns:
        Dictionary representing the models.yaml structure
    """
    lines = input_text.strip().split('\n')
    # Extract headers (first line)
    headers = [h.strip() for h in lines[0].split('\t')]
    
    # Process each data line
    entries = {}
    for line in lines[1:]:
        if not line.strip():
            continue
            
        values = line.split('\t')
        row_data = {headers[i]: values[i].strip() if i < len(values) else "" 
                    for i in range(len(headers))}
        
        # Skip entries without a name
        if not row_data.get("Schema") and not row_data.get("org/repo"):
            continue
            
        entry_name = row_data.get("Schema", "").strip()
        if not entry_name:
            entry_name = row_data.get("org/repo", "").strip()
        
        # Check if it's a valid schema
        schema_type = row_data.get("Type", "").strip()
        if schema_type and "Not a Schema" in schema_type:
            continue
        
        # Create entry
        entry = {}
        
        # Map fields
        if row_data.get("org/repo"):
            entry["github_repo"] = "https://github.com/"+row_data["org/repo"]

        if row_data.get("Source URL (GitHub Preferred)"):
            entry["schema_url"] = row_data["Source URL (GitHub Preferred)"]
            
        if row_data.get("Description"):
            entry["description"] = row_data["Description"]
            
        if row_data.get("Schema"):
            entry["title"] = row_data["Schema"]
            
        if row_data.get("Primary Technical Contacts"):
            entry["contacts"] = row_data["Primary Technical Contacts"]
            
        if row_data.get("Domain"):
            domains = [d.strip() for d in row_data["Domain"].split(',')]
            entry["domain"] = domains if len(domains) > 1 else row_data["Domain"]
            
        if row_data.get("Status") and row_data["Status"] != "":
            entry["status"] = row_data["Status"]
            
        # Add topics if there are domains
        if row_data.get("Domain") and row_data["Domain"].strip():
            domains = [d.strip() for d in row_data["Domain"].split(',')]
            if domains and domains[0]:
                entry["topics"] = domains
        
        # Handle license
        entry["license"] = "CC-0"  # Default license
        
        # Clean up and validate the entry
        entry = {k: v for k, v in entry.items() if v}

        # Add the entry to the entries dictionary using org/repo as the key
        if entry:  # Only add if entry is not empty
            entry_key = row_data.get("org/repo", "").strip()
            if entry_key:
                entries[entry_key] = entry

    # Create the registry structure
    registry = {
        "name": "LinkML-Main-Registry",
        "homepage": "https://github.com/linkml/linkml-registry",
        "title": "This is the main LinkML registry",
        "entries": entries
    }
    
    return registry

def main():
    """Main function to read input and write output."""
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r') as file:
            input_text = file.read()
    else:
        # Read from stdin
        input_text = sys.stdin.read()
    
    registry = convert_data(input_text)

    # Check if entries were created
    if not registry["entries"]:
        print("WARNING: No entries were created. Check the input data format.", file=sys.stderr)
    else:
        print(f"Created {len(registry['entries'])} entries", file=sys.stderr)

    # Output as YAML
    yaml_text = yaml.dump(registry, sort_keys=False, default_flow_style=False)
    
    if len(sys.argv) > 2:
        # Write to file
        with open(sys.argv[2], 'w') as file:
            file.write(yaml_text)
    else:
        # Write to stdout
        print(yaml_text)

if __name__ == "__main__":
    main()