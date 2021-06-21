import argparse
import git
import gitutils


def deploy_branch(path_to_repo, branch_name, remote_url):
    remote_name = 'ad9055f94eb34ad2-90ccd5811527bc6e'
    repo = git.Repo(path_to_repo)

    if gitutils.has_branch(repo, branch_name) == False:
        repo_name = gitutils.get_repo_name_from_path(path_to_repo)
        print(f"  [Error] {repo_name} doesn't have '{branch_name}' branch.")
        return

    active_branch = repo.active_branch
    remote = repo.create_remote(remote_name, remote_url)
    repo.git.checkout(branch_name)
    remote.push(branch_name)
    repo.delete_remote(remote_name)
    repo.git.checkout(active_branch)
    print(f'  pushed: {branch_name} -> {remote_url}')


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True,
                        metavar='repository path', help='repository path')
    parser.add_argument('--url', required=True,
                        metavar='remote url', help='remote url')
    parser.add_argument('--branch', required=True,
                        metavar='branch name', help='branch name will be deployed')
    return parser.parse_args()


def main():
    args = parse_arguments()
    repo_name = gitutils.get_repo_name_from_path(args.path)
    print(f'{repo_name}/{args.branch} -> {args.url}')
    deploy_branch(args.path, args.branch, args.url)


if __name__ == '__main__':
    main()
