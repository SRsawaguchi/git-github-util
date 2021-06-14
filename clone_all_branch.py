import re
import argparse
import os
import git

def git_clone(url, dest, name):
    return git.Repo.clone_from(url, os.path.join(dest, name))

def get_repo_name_from_url(url):
    return url.removesuffix('.git').split('/')[-1]

def checkout_remote_branches(repo, remote='origin'):
    active_branch = repo.active_branch
    for ref in repo.references:
        prog = re.compile(r'.+/(.+)')
        if (ref.name.startswith(remote)):
            m = prog.match(ref.name)
            if not m:
                print(f'  - skip: {ref.name}');
                continue
            branch_name = m.group(1)
            if branch_name not in ['HEAD', 'main', 'master', active_branch]:
                print(f'  - checkout: {ref.name}')
                repo.git.checkout('-b', branch_name, ref.name)
    repo.git.checkout(active_branch)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, metavar='clone_url', help='clone url')
    parser.add_argument('--dest', required=True, metavar='output_directory', help='output directory')
    args = parser.parse_args()

    repo_name = get_repo_name_from_url(args.url)
    repo = git_clone(args.url, args.dest, repo_name)
    print(f'cloned {repo_name}')

    checkout_remote_branches(repo)

if __name__ == '__main__':
    main()
