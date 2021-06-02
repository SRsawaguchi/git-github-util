import os
from github import Github

# 表示するorganization
organization = ""

access_token = os.getenv('GITHUB_TOKEN')
gh = Github(access_token)

org = gh.get_organization(organization)

for repo in org.get_repos():
    print(repo.html_url)
