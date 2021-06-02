import os
from time import sleep

import github
import git
from github import Github

# 走査するディレクトリ
base_dir = ""
# リポジトリを作成するGitHubのOrganization
organization = ""

access_token = os.getenv('GITHUB_TOKEN')
gh = Github(access_token)

def is_git_repository(path):
    try:
        git.Repo(path)
        return True;
    except git.InvalidGitRepositoryError:
        return False

def create_repo_on_github(repo_name):
    org = gh.get_organization(organization)
    new_repo = org.create_repo(repo_name)
    return new_repo.clone_url


files = os.listdir(base_dir)

repo_directories = [f for f in files if is_git_repository(os.path.join(base_dir, f))]

for dir in repo_directories:
    print(dir)
    repo = git.Repo(os.path.join(base_dir, dir))

    repo.git.branch('-M', 'main')

    if repo.is_dirty():
        path_to_readme = os.path.join(repo.working_tree_dir, 'README.md')
        repo.index.add([path_to_readme])
        repo.index.commit('Update submission form url')
        print('--> commit README.md')

    remote_url = create_repo_on_github(dir)
    print('--> create repo: ' + remote_url)
    remote = repo.create_remote(organization, remote_url)
    remote.push('main')
    print('--> push main')

    for ref in repo.references:
        if 'solution' in ref.name:
            solution_branch = ref.name[7:]
            repo.git.checkout('-b', solution_branch, ref.name)
            remote.push(solution_branch)
            print('--> push ' + solution_branch)
    
    repo.git.checkout('main')
    print('--> checkout main')
    sleep(1)
