from .registry import SchemaRegistry, SchemaMetadata
from typing import Dict, List, Optional
from github import Github
import logging
import re
import subprocess
from pathlib import Path
import os


g = Github()

def get_repo(s: SchemaMetadata):
    repo_name = get_repo_name(s)
    if repo_name:
        print(f'Repo = {repo_name}')
        try:
            return g.get_repo(repo_name)
        except:
            logging.error(f'Error accessing {repo_name}')
            return None

def get_repo_name(s: SchemaMetadata) -> str:
    if s.github_repo is not None:
        return s.github_repo
    if s.schema_url is not None:
        m = re.search('github.com/([\\w-]+/[\\w-]+)/', s.schema_url)
        if m:
            return m.group(1)

def get_stars(s: SchemaMetadata) -> Optional[int]:
    repo = get_repo(s)
    print(f'Repo for {s.name} = {repo}')
    if repo:
        try:
            return repo.stargazers_count
        except:
            logging.error(f'Error accessing {repo}')

def get_repo_clone_url(s: SchemaMetadata):
    repo = get_repo_name(s)
    return f'https://github.com/{repo}.git'

def clone_repo(s: SchemaMetadata, workdir=None, replace=False) -> str:
    if workdir is None:
        workdir = 'tmp'
    [owner, repo] = get_repo_name(s).split('/')
    path = f'{workdir}/{repo}'
    print(f'{s.name} Path={path}')
    if os.path.exists(path):
        if replace:
            os.remove(path)
        else:
            return path
    url = get_repo_clone_url(s)
    Path(workdir).mkdir(parents=True, exist_ok=True)
    runcmds([f'cd {workdir}',
             f'git clone {url}'])
    return path



def runcmds(cmds: List[str]):
    return runcmd(" && ".join(cmds))

def runcmd(cmd):
    logging.info("RUNNING: {}".format(cmd))
    p = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    (out, err) = p.communicate()
    logging.info('OUT: {}'.format(out))
    if err:
        logging.error(err)
    if p.returncode != 0:
        raise Exception('Failed: {}'.format(cmd))