import os

import argparse
import git
import gitutils


def deploy_main_and_solution(
    repo_path,
    organization,
    default_branch_name="main",
    branch_protection=False,
):
    gh = gitutils.get_github()
    repo = git.Repo(repo_path)
    repo_name = os.path.basename(repo_path)
    repo.git.branch("-M", default_branch_name)

    print(repo_name)

    if repo.is_dirty():
        path_to_readme = os.path.join(repo.working_tree_dir, "README.md")
        repo.index.add([path_to_readme])
        repo.index.commit("Update README.md")
        print("--> commit README.md")

    remote_url = gitutils.create_repo_on_github(gh, repo_name, organization)
    print("--> create repo: " + remote_url)
    remote = repo.create_remote(organization, remote_url)
    remote.push(default_branch_name)
    print(f"--> push {default_branch_name}")

    did_solution_pushed = False
    for ref in repo.references:
        if "solution" in ref.name:
            if ref.name == "solution" or ref.name == "solutions":
                solution_branch = ref.name
                repo.git.checkout(solution_branch)
                remote.push(solution_branch)
                print("--> push " + solution_branch)
                did_solution_pushed = True

    if did_solution_pushed is False:
        print("--> There is no branch named `solution`.")

    repo.git.checkout(default_branch_name)
    print(f"--> checkout {default_branch_name}")

    if branch_protection:
        gitutils.add_branch_protection(gh, organization, repo_name, default_branch_name)
        print(f"--> branch protection rule added to {default_branch_name}")


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
        "--branch-protection",
        action="store_true",
        dest="branch_protection",
    )

    args = parser.parse_args()
    deploy_main_and_solution(
        repo_path=args.repo,
        organization=args.org,
        branch_protection=args.branch_protection,
    )


if __name__ == "__main__":
    main()
