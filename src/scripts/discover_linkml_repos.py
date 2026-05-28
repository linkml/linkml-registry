#!/usr/bin/env python3
"""
Discover LinkML projects using GitHub Search REST API.

Simple script that searches for repositories containing LinkML dependencies
in pyproject.toml and requirements.txt files.
"""

import os
import sys
import json
import random
import yaml
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any
import click
from datetime import datetime
import time
from enum import Enum


class RateLimitExhaustedError(RuntimeError):
    """Raised when GitHub rate-limit retries are exhausted for a single request."""


class ExcludeList(Enum):
    """
    Curated list of repository URLs to exclude from LinkML discovery.
    These are false positives that contain linkml-like terms but are not actual LinkML projects.
    """
    AWESOME_MACHINE_LEARNING = "https://github.com/josephmisiti/awesome-machine-learning"
    W3ID = "https://github.com/perma-id/w3id.org"
    WOC = "https://github.com/w3c/wot"


def extract_contacts(repo: Dict[str, Any]) -> Optional[str]:
    """Extract contact information."""
    owner = repo['owner']
    return owner.get('login', 'Unknown')


def generate_registry_yaml(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
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


def is_excluded_repository(repo: Dict[str, Any]) -> bool:
    """Check if repository should be excluded based on the curated exclude list."""
    repo_url = repo.get('html_url', '')

    # Check against each item in the exclude list
    for exclude_item in ExcludeList:
        if repo_url == exclude_item.value:
            print(f"  Excluded false positive: {repo['full_name']} (matched exclude list)")
            return True

    return False


class GitHubSearchDiscovery:
    """Discover LinkML projects using GitHub Search REST API."""
    
    # Retry/backoff configuration for GitHub rate limits.
    MAX_RETRIES = 5
    BACKOFF_SCHEDULE = [30, 60, 120, 300, 600]  # seconds, per retry attempt
    MAX_RESET_WAIT = 15 * 60  # cap on waiting for X-RateLimit-Reset, seconds

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
        # Queries that exhausted retries and were skipped. Inspected by the caller
        # to decide whether to fail the run.
        self.failed_queries: List[str] = []
        # Cache of /repos/{full_name} lookups. Value is None when the lookup
        # failed (and was recorded in failed_queries). Used both to avoid
        # duplicate API calls and to enrich the minimal repository objects that
        # GitHub returns for code-search / README-search results.
        self._repo_cache: Dict[str, Optional[Dict[str, Any]]] = {}

    def _compute_sleep_seconds(self, response: requests.Response, attempt: int) -> float:
        """Pick a sleep duration after a 403/429 based on response headers.

        Priority:
          1. Retry-After header (secondary rate limit / abuse detection).
          2. X-RateLimit-Reset when X-RateLimit-Remaining == 0 (primary limit).
          3. Exponential backoff schedule.
        Jitter is added to avoid synchronized retries.
        """
        retry_after = response.headers.get('Retry-After')
        if retry_after:
            try:
                return float(retry_after) + random.uniform(0, 2)
            except ValueError:
                pass

        remaining = response.headers.get('X-RateLimit-Remaining')
        reset = response.headers.get('X-RateLimit-Reset')
        if remaining is not None and reset is not None:
            try:
                if int(remaining) == 0:
                    wait = int(reset) - int(time.time())
                    if wait > 0:
                        return min(wait, self.MAX_RESET_WAIT) + random.uniform(0, 2)
            except ValueError:
                pass

        idx = min(attempt, len(self.BACKOFF_SCHEDULE) - 1)
        return self.BACKOFF_SCHEDULE[idx] + random.uniform(0, 5)

    def _proactive_throttle(self, response: requests.Response) -> None:
        """If we are about to exhaust the rate limit, sleep until reset."""
        remaining = response.headers.get('X-RateLimit-Remaining')
        reset = response.headers.get('X-RateLimit-Reset')
        if remaining is None or reset is None:
            return
        try:
            remaining_int = int(remaining)
            reset_int = int(reset)
        except ValueError:
            return
        if remaining_int < 3:
            wait = reset_int - int(time.time())
            if wait > 0:
                wait = min(wait, self.MAX_RESET_WAIT)
                print(f"  Rate limit nearly exhausted ({remaining_int} remaining); sleeping {wait}s until reset")
                time.sleep(wait + random.uniform(0, 2))

    def _request_with_retry(self, url: str, params: Optional[Dict[str, Any]] = None,
                            description: str = '') -> requests.Response:
        """GET ``url`` with retries that honor GitHub's rate-limit headers.

        Raises RateLimitExhaustedError after MAX_RETRIES rate-limited attempts.
        Raises requests.RequestException for non-rate-limit network errors after
        MAX_RETRIES.
        """
        last_response: Optional[requests.Response] = None
        last_exc: Optional[Exception] = None

        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
            except requests.RequestException as exc:
                last_exc = exc
                sleep_s = self.BACKOFF_SCHEDULE[min(attempt, len(self.BACKOFF_SCHEDULE) - 1)]
                print(f"  Network error on {description or url}: {exc}; retrying in {sleep_s}s "
                      f"(attempt {attempt + 1}/{self.MAX_RETRIES})")
                time.sleep(sleep_s + random.uniform(0, 5))
                continue

            last_response = response

            if response.status_code in (403, 429):
                # Distinguish rate limit from a real 403 (e.g. permission denied).
                body_msg = ''
                try:
                    body_msg = (response.json().get('message') or '').lower()
                except (ValueError, AttributeError):
                    body_msg = ''
                is_rate_limit = (
                    response.status_code == 429
                    or 'rate limit' in body_msg
                    or 'abuse detection' in body_msg
                    or response.headers.get('X-RateLimit-Remaining') == '0'
                    or response.headers.get('Retry-After') is not None
                )
                if not is_rate_limit:
                    # A real 403 (e.g. forbidden); do not retry.
                    return response

                sleep_s = self._compute_sleep_seconds(response, attempt)
                kind = 'secondary' if 'abuse' in body_msg or 'secondary' in body_msg else 'primary'
                print(f"  Hit GitHub {kind} rate limit on {description or url} "
                      f"(status {response.status_code}); sleeping {sleep_s:.1f}s "
                      f"(attempt {attempt + 1}/{self.MAX_RETRIES})")
                time.sleep(sleep_s)
                continue

            # Success or non-rate-limit error: let caller decide.
            self._proactive_throttle(response)
            return response

        if last_response is not None:
            raise RateLimitExhaustedError(
                f"Rate limit retries exhausted for {description or url}: "
                f"last status {last_response.status_code}"
            )
        raise RateLimitExhaustedError(
            f"Network retries exhausted for {description or url}: {last_exc}"
        )

    def _fetch_full_repo(self, full_name: str) -> Optional[Dict[str, Any]]:
        """Fetch canonical repo metadata via /repos/{full_name}.

        Results are cached so the same repo is not refetched across the many
        code-search queries that may surface it. Returns None on failure (rate
        limit exhausted, 404, network error). The minimal repository object
        embedded in code-search results lacks stargazers_count, license,
        archived, and topics, so we need this to get accurate metadata.
        """
        if full_name in self._repo_cache:
            return self._repo_cache[full_name]

        url = f"{self.base_url}/repos/{full_name}"
        try:
            response = self._request_with_retry(
                url, description=f"repo metadata {full_name}"
            )
        except RateLimitExhaustedError as exc:
            print(f"  Rate limit hit fetching {full_name}: {exc}")
            self.failed_queries.append(f"repo-meta:{full_name}")
            self._repo_cache[full_name] = None
            return None
        except requests.RequestException as exc:
            print(f"  Network error fetching {full_name}: {exc}")
            self._repo_cache[full_name] = None
            return None

        if response.status_code != 200:
            print(f"  Failed to fetch {full_name}: HTTP {response.status_code}")
            self._repo_cache[full_name] = None
            return None

        try:
            data = response.json()
        except ValueError:
            self._repo_cache[full_name] = None
            return None

        self._repo_cache[full_name] = data
        return data

    def search_linkml_repositories(self) -> List[Dict[str, Any]]:
        """Search for repositories that have LinkML dependencies."""
        
        all_repos = {}  # Use dict to deduplicate by full_name
        
        # First, do general repository searches using REST API
        repo_search_queries = [
            "linkml language:python",  # Quoted to avoid FlinkML
            "linkml-project-cookiecutter",
            "linkml in:description",  # Quoted to avoid FlinkML
            "LinkML in:description"   # Quoted to avoid FlinkML
        ]
        
        for query in repo_search_queries:
            print(f"Repository search: {query}")
            repos = self._search_repositories(query)
            
            for repo in repos:
                full_name = repo['full_name']
                # Skip repos from the linkml organization itself
                if full_name.startswith('linkml/'):
                    print(f"  Skipped linkml org repo: {full_name}")
                    continue
                # Skip excluded repositories
                if is_excluded_repository(repo):
                    continue
                if full_name not in all_repos and not repo.get('fork', False):
                    all_repos[full_name] = repo
                    stars = repo.get('stargazers_count', 0)
                    print(f"  Found: {full_name} ({stars} stars)")
                elif repo.get('fork', False):
                    print(f"  Skipped fork: {full_name}")
            
            # Conservative rate limiting for REST API
            time.sleep(5)
        
        # Search README files for LinkML content using code search
        if self.token:
            readme_search_queries = [
                "linkml",  # Exact match with quotes to avoid FlinkML
                "LinkML",  # Exact match with quotes to avoid FlinkML
                "linkml-project-cookiecutter"
            ]
            
            for query in readme_search_queries:
                print(f"README search: {query}")
                code_results = self._search_readme_content(query)

                for result in code_results:
                    minimal_repo = result.get('repository', {})
                    full_name = minimal_repo.get('full_name', '')

                    if not full_name:
                        continue

                    # Skip repos from the linkml organization itself
                    if full_name.startswith('linkml/'):
                        print(f"  Skipped linkml org repo: {full_name}")
                        continue

                    # The README/code-search "repository" object lacks stars,
                    # license, archived, and topics; enrich via /repos/{name}.
                    repo = self._fetch_full_repo(full_name) or minimal_repo

                    # Skip excluded repositories
                    if is_excluded_repository(repo):
                        continue

                    if full_name not in all_repos and not repo.get('fork', False):
                        all_repos[full_name] = repo
                        stars = repo.get('stargazers_count', 0) or 0
                        print(f"  Found in README: {full_name} ({stars} stars)")
                    elif repo.get('fork', False):
                        print(f"  Skipped fork: {full_name}")

                # Conservative rate limiting for code search
                time.sleep(10)

        # Then, search for linkml in specific files using REST code search
        if self.token:
            file_search_queries = [
                "linkml filename:pyproject.toml",
                "LinkML filename:pyproject.toml",
                "Linkml filename:pyproject.toml",
                "schema-automator filename:pyproject.toml",
                "dependencies schema-automator filename:pyproject.toml",
                "dependencies linkml filename:pyproject.toml",
                "description linkml filename:pyproject.toml",
                "description LinkML filename:pyproject.toml",
                "description Linkml filename:pyproject.toml",
                "linkml filename:requirements.txt",
                "schema-automator filename:requirements.txt",
                "linkml filename:setup.py",
                "schema-automator filename:setup.py",
                "linkml filename:setup.cfg",
                "schema-automator filename:setup.cfg",
                "linkml filename:poetry.lock",
                "schema-automator filename:poetry.lock",
                "linkml filename:Pipfile",
                "schema-automator filename:Pipfile",
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
                    # Skip repos from the linkml organization itself
                    if full_name.startswith('linkml/'):
                        print(f"  Skipped linkml org repo: {full_name}")
                        continue
                    # Skip excluded repositories
                    if is_excluded_repository(repo):
                        continue
                    if full_name not in all_repos and not repo.get('fork', False):
                        all_repos[full_name] = repo
                        stars = repo.get('stargazers_count', 0)
                        print(f"  Found: {full_name} ({stars} stars)")
                    elif repo.get('fork', False):
                        print(f"  Skipped fork: {full_name}")
                
                # Conservative rate limiting for code search (stricter limits than repo search)
                time.sleep(10)
        else:
            print("Skipping file searches - requires GitHub token for code search API")
        
        print(f"\nTotal unique repositories found: {len(all_repos)}")
        if self.failed_queries:
            print(f"\nWARNING: {len(self.failed_queries)} search queries were dropped after exhausting retries:")
            for q in self.failed_queries:
                print(f"  - {q}")
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
            response = self._request_with_retry(url, params=params,
                                                description=f"repo search '{query}'")
        except RateLimitExhaustedError as exc:
            print(f"  {exc}")
            self.failed_queries.append(f"repo:{query}")
            return []
        except requests.RequestException as exc:
            print(f"  Error searching for '{query}': {exc}")
            self.failed_queries.append(f"repo:{query}")
            return []

        if response.status_code != 200:
            print(f"  Search failed for query '{query}': {response.status_code}")
            return []

        try:
            data = response.json()
        except ValueError as exc:
            print(f"  Invalid JSON for query '{query}': {exc}")
            return []
        return data.get('items', [])
    
    def _search_readme_content(self, search_string: str, per_page: int = 30) -> List[Dict[str, Any]]:
        """Search for a string in README.md files using GitHub's code search API."""

        if not self.token:
            return []

        url = f"{self.base_url}/search/code"
        query = f"{search_string} in:file filename:README.md"
        params = {
            'q': query,
            'per_page': per_page
        }

        try:
            response = self._request_with_retry(url, params=params,
                                                description=f"readme search '{query}'")
        except RateLimitExhaustedError as exc:
            print(f"  {exc}")
            self.failed_queries.append(f"readme:{query}")
            return []
        except requests.RequestException as exc:
            print(f"  Error searching for '{query}': {exc}")
            self.failed_queries.append(f"readme:{query}")
            return []

        if response.status_code == 422:
            print(f"  README search query invalid: {query}")
            return []
        if response.status_code != 200:
            print(f"  Search failed for query '{query}': {response.status_code}")
            return []

        try:
            data = response.json()
        except ValueError as exc:
            print(f"  Invalid JSON for query '{query}': {exc}")
            return []
        return data.get('items', [])
    
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
            response = self._request_with_retry(url, params=params,
                                                description=f"code search '{query}'")
        except RateLimitExhaustedError as exc:
            print(f"  {exc}")
            self.failed_queries.append(f"code:{query}")
            return []
        except requests.RequestException as exc:
            print(f"  Error in code search for '{query}': {exc}")
            self.failed_queries.append(f"code:{query}")
            return []

        if response.status_code == 422:
            print(f"  Code search query invalid: {query}")
            return []
        if response.status_code != 200:
            print(f"  Code search failed for query '{query}': {response.status_code}")
            return []

        try:
            data = response.json()
        except ValueError as exc:
            print(f"  Invalid JSON in code search for '{query}': {exc}")
            return []

        # Extract unique repositories from code search results.
        # The repository object embedded in code-search results is heavily
        # stripped down (no stargazers_count, license, archived, or topics),
        # so we enrich each one via /repos/{full_name}.
        repos = []
        repo_names_seen = set()

        for item in data.get('items', []):
            repo_data = item['repository']
            repo_name = repo_data['full_name']

            # Skip if we've already processed this repository
            if repo_name in repo_names_seen:
                continue
            repo_names_seen.add(repo_name)

            full = self._fetch_full_repo(repo_name)
            if full is not None:
                repos.append(full)
            else:
                # Enrichment failed; fall back to the minimal record so we at
                # least keep the discovery hit. The failed lookup is already
                # tracked in failed_queries and will trigger the fail-on-rate-
                # limit guard at the end of the run.
                repos.append({
                    'name': repo_data['name'],
                    'full_name': repo_data['full_name'],
                    'description': repo_data.get('description'),
                    'html_url': repo_data['html_url'],
                    'stargazers_count': repo_data.get('stargazers_count', 0) or 0,
                    'archived': bool(repo_data.get('archived')),
                    'private': bool(repo_data.get('private')),
                    'size': repo_data.get('size', 0),
                    'updated_at': repo_data.get('updated_at'),
                    'homepage': repo_data.get('homepage'),
                    'topics': repo_data.get('topics') or [],
                    'language': repo_data.get('language'),
                    'license': repo_data.get('license'),
                    'owner': repo_data.get('owner', {}),
                })

        print(f"  Found {len(repos)} unique repositories")
        return repos
    
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
        contacts = extract_contacts(repo)
        if contacts:
            entry['contacts'] = contacts
        
        # Stars: enrichment in the search phase already replaced the stripped
        # code-search repo object with the canonical /repos/{name} response,
        # so this is reliable. If enrichment failed for this repo, the missing
        # data will have been recorded in failed_queries and the run will exit
        # non-zero downstream.
        stars = repo.get('stargazers_count') or 0
        entry['github_stars'] = stars

        return entry
    
    def _extract_license(self, repo: Dict[str, Any]) -> str:
        """Extract license information."""
        license_info = repo.get('license')
        # If license is not available, return 'Unknown'
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


@click.command()
@click.option('--token', help='GitHub personal access token (or set GITHUB_TOKEN or GH_TOKEN env var)')
@click.option('--output', required=True, help='Output file for discovered registry')
@click.option('--min-stars', default=1, help='Minimum stars required (default: 1)')
@click.option('--analyze/--no-analyze', default=True, help='Whether to analyze repositories for metadata')
@click.option('--fail-on-rate-limit/--no-fail-on-rate-limit', default=True,
              help='Exit non-zero if any search query was dropped due to rate limits '
                   '(default: enabled; disable for best-effort local runs)')
def main(token, output, min_stars, analyze, fail_on_rate_limit):
    """Discover LinkML projects using GitHub Search REST API."""

    try:
        discovery = GitHubSearchDiscovery(token)

        print("Starting LinkML project discovery...")
        repos = discovery.search_linkml_repositories()

        if not repos:
            print("No repositories found!")
            if fail_on_rate_limit and discovery.failed_queries:
                print(f"ERROR: {len(discovery.failed_queries)} queries were dropped "
                      f"due to rate limits; refusing to publish empty result.")
                sys.exit(2)
            return
        
        # Filter by stars
        if min_stars > 0:
            repos = [r for r in repos if r.get('stargazers_count', 0) >= min_stars]
            print(f"\n Filtered to {len(repos)} repos with >= {min_stars} stars")
        
        if not analyze:
            # Quick mode - just basic info
            registry_entries = []
            for repo in repos:
                entry = {
                    'title': repo['name'],
                    'description': repo.get('description', ''),
                    'github_repo': repo['html_url'],
                    'license': discovery._extract_license(repo),
                    'github_stars': repo.get('stargazers_count', 0)
                }
                registry_entries.append(entry)
            
            registry = generate_registry_yaml(registry_entries)
        else:
            # Full analysis mode
            print(f"\n Analyzing {len(repos)} repositories...")
            registry_entries = []
            
            for i, repo in enumerate(repos, 1):
                # Show progress
                print(f"[{i:2d}/{len(repos)}] ", end="")
                entry = discovery.analyze_repository(repo)
                if entry:
                    registry_entries.append(entry)
            
            print(f"\n Successfully analyzed {len(registry_entries)} repositories")
            registry = generate_registry_yaml(registry_entries)
        
        # Write output
        output_path = Path(output)
        with open(output_path, 'w') as f:
            yaml.dump(registry, f, default_flow_style=False, sort_keys=False, width=120)
        
        print(f"\n Registry saved to {output_path}")
        print(f"\n Total LinkML projects: {len(registry['entries'])}")
        
        # Show some stats
        if registry['entries']:
            licenses = {}
            domains = {}
            for entry in registry['entries'].values():
                license_key = entry.get('license', 'Unknown')
                licenses[license_key] = licenses.get(license_key, 0) + 1
                
                domain_key = entry.get('domain', 'Unknown')
                domains[domain_key] = domains.get(domain_key, 0) + 1
            
            print(f"\n License distribution: {dict(sorted(licenses.items(), key=lambda x: x[1], reverse=True))}")
            print(f"\n Domain distribution: {dict(sorted(domains.items(), key=lambda x: x[1], reverse=True))}")

        if fail_on_rate_limit and discovery.failed_queries:
            print(f"\nERROR: {len(discovery.failed_queries)} search queries were dropped "
                  f"due to GitHub rate limits. The registry produced by this run is "
                  f"likely incomplete; refusing to publish. "
                  f"Re-run later or pass --no-fail-on-rate-limit to override.")
            sys.exit(2)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()