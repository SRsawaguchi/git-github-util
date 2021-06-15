import argparse
import git
import gitutils


def deploy_repo(path_to_repo, organization, remote_name):
    gh = gitutils.get_github()
    repo = git.Repo(path_to_repo)
    repo_name = gitutils.get_repo_name_from_path(path_to_repo)
    remote_url = gitutils.create_repo_on_github(gh, repo_name, organization)
    print(f'repo: {repo_name}')
    print(f'  -- remote: {remote_url}')
    repo.create_remote(remote_name, remote_url)
    gitutils.push_all_branch(repo, remote_name)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True,
                        metavar='repository path', help='repository path')
    parser.add_argument('--org', required=True,
                        metavar='organization', help='organization')
    parser.add_argument('--remote', required=True,
                        metavar='remote name', help='remote name')
    return parser.parse_args()


def main():
    args = parse_arguments()
    deploy_repo(args.path, args.org, args.remote)


if __name__ == '__main__':
    main()
