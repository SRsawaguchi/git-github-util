import re
import os
import git
import github


def is_git_repository(path):
    try:
        git.Repo(path)
        return True
    except git.InvalidGitRepositoryError:
        return False


def git_clone(url, dest, name):
    return git.Repo.clone_from(url, os.path.join(dest, name))


def get_repo_name_from_url(url):
    return url.removesuffix('.git').split('/')[-1]


def get_repo_name_from_path(path):
    return path.split('/')[-1]


def checkout_remote_branches(repo, remote='origin'):
    active_branch = repo.active_branch
    for ref in repo.references:
        prog = re.compile(r'.+/(.+)')
        if (ref.name.startswith(remote)):
            m = prog.match(ref.name)
            if not m:
                print(f'  - skip: {ref.name}')
                continue
            branch_name = m.group(1)
            if branch_name not in ['HEAD', 'main', 'master', active_branch]:
                print(f'  - checkout: {ref.name}')
                repo.git.checkout('-b', branch_name, ref.name)
    repo.git.checkout(active_branch)


def get_github(token='', hostname=''):
   if not token:
       token = os.getenv('GITHUB_TOKEN')
   if not hostname:
       return github.Github(token)
   else:
       return github.Github(token, base_url=f'https://{hostname}/api/v3')


def create_repo_on_github(github, repo_name, organization):
    org = github.get_organization(organization)
    new_repo = org.create_repo(repo_name, private=True)
    return new_repo.clone_url


def push_all_branch(repo, remote_name):
    remote = repo.remotes[remote_name]
    for branch in repo.branches:
        print(f'  -- push: {remote_name}/{branch}')
        remote.push(branch)


def has_branch(repo, branch_name):
    branch = next(
        (ref.name for ref in repo.references if ref.name == branch_name), None)
    return branch != None
