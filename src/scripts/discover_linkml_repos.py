#!/usr/bin/env python3
"""
Discover LinkML projects using GitHub Search REST API.

Simple script that searches for repositories containing LinkML dependencies
in pyproject.toml and requirements.txt files.
"""

import os
import sys
import json
import yaml
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any
import click
from datetime import datetime
import time


class GitHubSearchDiscovery:
    """Discover LinkML projects using GitHub Search REST API."""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize with GitHub token."""
        self.token = token or os.getenv('GITHUB_TOKEN') or os.getenv('GH_TOKEN')
        if not self.token:
            print("Warning: No GitHub token provided. Rate limits will be lower.")
            self.headers = {}
        else:
            self.headers = {
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            }
        
        self.base_url = 'https://api.github.com'
    
    def search_linkml_repositories(self) -> List[Dict[str, Any]]:
        """Search for repositories that have LinkML dependencies."""
        
        all_repos = {}  # Use dict to deduplicate by full_name
        
        # First, do general repository searches using REST API
        repo_search_queries = [
            "linkml language:python",
            "linkml-project-cookiecutter",
            "linkml in:description",
            "LinkML in:description"
        ]
        
        for query in repo_search_queries:
            print(f"Repository search: {query}")
            repos = self._search_repositories(query)
            
            for repo in repos:
                full_name = repo['full_name']
                if full_name not in all_repos and not repo.get('fork', False):
                    all_repos[full_name] = repo
                    print(f"  Found: {full_name} ({repo['stargazers_count']} stars)")
                elif repo.get('fork', False):
                    print(f"  Skipped fork: {full_name}")
            
            # Conservative rate limiting for REST API
            time.sleep(2)
        
        # Then, search for linkml in specific files using REST code search
        if self.token:
            file_search_queries = [
                "linkml filename:pyproject.toml",
                "linkml filename:requirements.txt", 
                "linkml filename:setup.py",
                "linkml filename:setup.cfg",
                "linkml filename:poetry.lock",
                "linkml filename:Pipfile",
                "linkml-project-cookiecutter filename:README.md",
                "linkml-project-cookiecutter filename:README.rst",
                "linkml-project-cookiecutter filename:readme.md",
                "linkml filename:README.md",
                "LinkML filename:README.md",
                "linkml filename:README.rst",
                "LinkML filename:README.rst",
            ]
            
            for query in file_search_queries:
                print(f"Code search: {query}")
                repos = self._search_code_rest(query)
                
                for repo in repos:
                    full_name = repo['full_name']
                    if full_name not in all_repos and not repo.get('fork', False):
                        all_repos[full_name] = repo
                        print(f"  Found: {full_name} ({repo.get('stargazers_count', 0)} stars)")
                    elif repo.get('fork', False):
                        print(f"  Skipped fork: {full_name}")
                
                # Conservative rate limiting for code search (stricter limits than repo search)
                time.sleep(6)
        else:
            print("Skipping file searches - requires GitHub token for code search API")
        
        print(f"\nTotal unique repositories found: {len(all_repos)}")
        return list(all_repos.values())
    
    def _search_repositories(self, query: str, per_page: int = 50) -> List[Dict[str, Any]]:
        """Execute repository search using GitHub Search API."""
        
        url = f"{self.base_url}/search/repositories"
        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': per_page
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 403:
                print(f"  Rate limit exceeded for query: {query}")
                return []
            elif response.status_code != 200:
                print(f"  Search failed for query '{query}': {response.status_code}")
                return []
            
            data = response.json()
            return data.get('items', [])
            
        except Exception as e:
            print(f"  Error searching for '{query}': {e}")
            return []
    
    def _search_code_rest(self, query: str, per_page: int = 20) -> List[Dict[str, Any]]:
        """Search for code using GitHub REST API code search."""
        
        if not self.token:
            return []
        
        url = f"{self.base_url}/search/code"
        params = {
            'q': query,
            'sort': 'indexed',
            'order': 'desc',
            'per_page': per_page
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 403:
                print(f"  Rate limit exceeded for code search: {query}")
                print(f"  Waiting 60 seconds before continuing...")
                time.sleep(60)
                return []
            elif response.status_code == 422:
                print(f"  Code search query invalid: {query}")
                return []
            elif response.status_code != 200:
                print(f"  Code search failed for query '{query}': {response.status_code}")
                return []
            
            data = response.json()
            
            # Check rate limit headers
            rate_limit_remaining = response.headers.get('X-RateLimit-Remaining')
            if rate_limit_remaining and int(rate_limit_remaining) < 5:
                print(f"  Code search rate limit low ({rate_limit_remaining} remaining), slowing down...")
                time.sleep(10)
            
            # Extract unique repositories from code search results
            repos = []
            repo_names_seen = set()
            
            for item in data.get('items', []):
                repo_data = item['repository']
                repo_name = repo_data['full_name']
                
                # Skip if we've already processed this repository
                if repo_name in repo_names_seen:
                    continue
                repo_names_seen.add(repo_name)
                
                # Convert to standard format
                repo = {
                    'name': repo_data['name'],
                    'full_name': repo_data['full_name'],
                    'description': repo_data.get('description'),
                    'html_url': repo_data['html_url'],
                    'stargazers_count': repo_data.get('stargazers_count', 0),
                    'archived': repo_data.get('archived', False),
                    'private': repo_data.get('private', False),
                    'size': repo_data.get('size', 0),
                    'updated_at': repo_data.get('updated_at'),
                    'homepage': repo_data.get('homepage'),
                    'topics': repo_data.get('topics', []),
                    'language': repo_data.get('language'),
                    'license': repo_data.get('license'),
                    'owner': repo_data.get('owner', {})
                }
                repos.append(repo)
            
            print(f"  Found {len(repos)} unique repositories")
            return repos
            
        except Exception as e:
            print(f"  Error in code search for '{query}': {e}")
            return []
    
    def analyze_repository(self, repo: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze a repository to extract LinkML project information."""
        
        # Skip only archived repositories
        if repo.get('archived'):
            return None
        
        print(f"Analyzing: {repo['full_name']}")
        
        # Extract basic information
        entry = {
            'title': repo['name'],
            'description': (repo.get('description') or '').strip(),
            'github_repo': repo['html_url'],
            'license': self._extract_license(repo),
            'domain': self._extract_domain(repo),
            'status': self._determine_status(repo),
            'topics': self._extract_topics(repo)
        }
        
        # Try to find schema URL
        schema_url = self._find_schema_url(repo)
        if schema_url:
            entry['schema_url'] = schema_url
        
        # Extract contacts
        contacts = self._extract_contacts(repo)
        if contacts:
            entry['contacts'] = contacts
        
        # Add GitHub stars for sorting
        entry['github_stars'] = repo.get('stargazers_count', 0)
        
        return entry
    
    def _extract_license(self, repo: Dict[str, Any]) -> str:
        """Extract license information."""
        license_info = repo.get('license')
        if license_info and license_info.get('spdx_id'):
            return license_info['spdx_id']
        return 'Unknown'
    
    def _extract_domain(self, repo: Dict[str, Any]) -> str:
        """Determine domain based on repository metadata."""
        
        description = ((repo.get('description') or '') + ' ' + repo['name']).lower()
        topics = [topic.lower() for topic in repo.get('topics', [])]
        all_text = ' '.join([description] + topics)
        
        # Domain classification based on keywords
        domain_keywords = {
            'Biology': ['bio', 'genomics', 'life-science', 'molecular', 'genetics', 'omics'],
            'Clinical': ['clinical', 'medical', 'health', 'patient', 'diagnosis'],
            'Chemistry': ['chemistry', 'chemical', 'molecule', 'compound'],
            'Neuroscience': ['neuro', 'brain', 'neural', 'cognitive'],
            'Computer Science': ['data-science', 'ml', 'ai', 'software', 'algorithm'],
            'Energy': ['energy', 'power', 'grid', 'electrical'],
            'Government': ['gov', 'government', 'public', 'policy'],
            'Cancer': ['cancer', 'oncology', 'tumor'],
            'Infrastructure': ['infrastructure', 'network', 'system']
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                return domain
        
        return 'Schema'  # Default
    
    def _determine_status(self, repo: Dict[str, Any]) -> str:
        """Determine project status based on repository activity."""
        
        if repo.get('archived'):
            return 'archived'
        
        # Parse last update
        try:
            from datetime import datetime
            updated_at = datetime.fromisoformat(repo['updated_at'].replace('Z', '+00:00'))
            now = datetime.now(updated_at.tzinfo)
            days_since_update = (now - updated_at).days
            
            if days_since_update > 365:
                return 'inactive'
            elif days_since_update > 180:
                return 'maintenance'
            else:
                return 'active'
        except:
            return 'unknown'
    
    def _extract_topics(self, repo: Dict[str, Any]) -> List[str]:
        """Extract and clean repository topics."""
        topics = repo.get('topics', [])
        
        # Filter out generic topics
        generic_topics = {'python', 'yaml', 'json', 'api', 'library', 'tool', 'framework'}
        filtered_topics = [topic for topic in topics if topic.lower() not in generic_topics]
        
        return filtered_topics[:5]  # Limit to 5 most relevant topics
    
    def _find_schema_url(self, repo: Dict[str, Any]) -> Optional[str]:
        """Try to find the schema documentation URL."""
        
        # Check homepage URL
        homepage = repo.get('homepage')
        if homepage and any(indicator in homepage.lower() 
                           for indicator in ['github.io', 'docs', 'schema', 'w3id.org']):
            return homepage
        
        # Generate likely GitHub Pages URL
        owner_login = repo['owner']['login']
        repo_name = repo['name']
        
        # Common patterns for LinkML documentation
        possible_urls = [
            f"https://{owner_login.lower()}.github.io/{repo_name}/",
            f"https://{owner_login.lower()}.github.io/{repo_name}/docs/",
            f"https://w3id.org/{owner_login.lower()}/{repo_name}"
        ]
        
        # Return the first plausible URL (we can't easily verify without making requests)
        return possible_urls[0]
    
    def _extract_contacts(self, repo: Dict[str, Any]) -> Optional[str]:
        """Extract contact information."""
        owner = repo['owner']
        return owner.get('login', 'Unknown')
    
    def generate_registry_yaml(self, entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate the registry YAML structure."""
        
        # Sort entries by GitHub stars (descending), then alphabetically by title
        sorted_entries = sorted(entries, key=lambda x: (-x.get('github_stars', 0), x.get('title', '').lower()))
        
        # Convert entries to registry format
        registry_entries = {}
        
        for entry in sorted_entries:
            # Use owner/repo as the key
            github_url = entry.get('github_repo', '')
            if 'github.com/' in github_url:
                key = github_url.split('github.com/')[-1]
            else:
                key = entry.get('title', 'unknown')
            
            # Clean up the entry
            clean_entry = {k: v for k, v in entry.items() if v and v != 'Unknown'}
            registry_entries[key] = clean_entry
        
        registry = {
            'name': 'LinkML-Discovery-Registry',
            'homepage': 'https://github.com/linkml/linkml-registry',
            'title': 'LinkML Registry (GitHub Search Discovery)',
            'description': f'LinkML projects discovered via GitHub Search API. Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            'entries': registry_entries
        }
        
        return registry


@click.command()
@click.option('--token', help='GitHub personal access token (or set GITHUB_TOKEN or GH_TOKEN env var)')
@click.option('--output', required=True, help='Output file for discovered registry')
@click.option('--min-stars', default=1, help='Minimum stars required (default: 1)')
@click.option('--analyze/--no-analyze', default=True, help='Whether to analyze repositories for metadata')
def main(token, output, min_stars, analyze):
    """Discover LinkML projects using GitHub Search REST API."""
    
    try:
        discovery = GitHubSearchDiscovery(token)
        
        print("🚀 Starting LinkML project discovery...")
        repos = discovery.search_linkml_repositories()
        
        if not repos:
            print("❌ No repositories found!")
            return
        
        # Filter by stars
        if min_stars > 0:
            repos = [r for r in repos if r.get('stargazers_count', 0) >= min_stars]
            print(f"📊 Filtered to {len(repos)} repos with >= {min_stars} stars")
        
        if not analyze:
            # Quick mode - just basic info
            registry_entries = []
            for repo in repos:
                entry = {
                    'title': repo['name'],
                    'description': repo.get('description', ''),
                    'github_repo': repo['html_url'],
                    'license': discovery._extract_license(repo),
                    'stars': repo.get('stargazers_count', 0)
                }
                registry_entries.append(entry)
            
            registry = discovery.generate_registry_yaml(registry_entries)
        else:
            # Full analysis mode
            print(f"\n🔬 Analyzing {len(repos)} repositories...")
            registry_entries = []
            
            for i, repo in enumerate(repos, 1):
                print(f"[{i:2d}/{len(repos)}] ", end="")
                entry = discovery.analyze_repository(repo)
                if entry:
                    registry_entries.append(entry)
            
            print(f"\n✅ Successfully analyzed {len(registry_entries)} repositories")
            registry = discovery.generate_registry_yaml(registry_entries)
        
        # Write output
        output_path = Path(output)
        with open(output_path, 'w') as f:
            yaml.dump(registry, f, default_flow_style=False, sort_keys=False, width=120)
        
        print(f"\n🎉 Registry saved to {output_path}")
        print(f"📈 Total LinkML projects: {len(registry['entries'])}")
        
        # Show some stats
        if registry['entries']:
            licenses = {}
            domains = {}
            for entry in registry['entries'].values():
                license_key = entry.get('license', 'Unknown')
                licenses[license_key] = licenses.get(license_key, 0) + 1
                
                domain_key = entry.get('domain', 'Unknown')
                domains[domain_key] = domains.get(domain_key, 0) + 1
            
            print(f"\n📊 License distribution: {dict(sorted(licenses.items(), key=lambda x: x[1], reverse=True))}")
            print(f"📊 Domain distribution: {dict(sorted(domains.items(), key=lambda x: x[1], reverse=True))}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()