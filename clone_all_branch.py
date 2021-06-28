import argparse
import gitutils
import os
import re
import sys
import time

def checkout_remote_branches(repo, remote='origin'):
    active_branch = repo.active_branch
    for ref in repo.references:
        prog = re.compile(r'\w+/(\w+/?.+)')
        if (ref.name.startswith(remote)):
            m = prog.match(ref.name)
            if not m:
                print(f'  - skip: {ref.name}')
                continue
            branch_name = m.group(1)
            if branch_name not in ['HEAD']:
                if gitutils.has_branch(repo, branch_name):
                    print(f'  - skip: branch "{ref.name}" is already exists.')
                else:
                    print(f'  - checkout: {ref.name}')
                    repo.git.checkout('-b', branch_name, ref.name)
    repo.git.checkout(active_branch)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True,
                        metavar='clone_url', help='clone url')
    parser.add_argument('--dest', required=True,
                        metavar='output_directory', help='output directory')
    args = parser.parse_args()

    repo_name = gitutils.get_repo_name_from_url(args.url)
    print(repo_name)

    path_to_repo = os.path.join(args.dest, repo_name)
    if os.path.exists(path_to_repo):
        print(f'  -- skip: path already exists: {path_to_repo}')
        sys.exit(1)

    repo = gitutils.git_clone(args.url, args.dest, repo_name)
    print(f'cloned {repo_name}: {path_to_repo}')

    checkout_remote_branches(repo)


if __name__ == '__main__':
    main()
