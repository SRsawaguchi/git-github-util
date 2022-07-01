import argparse
import gitutils


def add_branch_protection(
    organization,
    repo_name,
    branch_name,
):
    gh = gitutils.get_github()
    gitutils.add_branch_protection(gh, organization, repo_name, branch_name)
    print(f"{organization}/{repo_name} - {branch_name}")
    print(f"--> branch protection rule added to {branch_name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        required=True,
        metavar="repository",
        help="path to repository",
    )
    parser.add_argument(
        "--org",
        required=True,
        metavar="organization",
    )
    parser.add_argument(
        "--branch",
        metavar="branch",
        default="main",
        help="branch name to protect",
    )

    args = parser.parse_args()
    add_branch_protection(args.org, args.repo, args.branch)


if __name__ == "__main__":
    main()
    import time

    time.sleep(1)
