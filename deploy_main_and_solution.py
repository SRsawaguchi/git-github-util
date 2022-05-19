import os

import argparse
import git
import gitutils


def deploy_main_and_solution(repo_path, organization, default_branch_name="main"):
    gh = gitutils.get_github()
    repo = git.Repo(repo_path)
    repo_name = os.path.basename(repo_path)
    repo.git.branch("-M", default_branch_name)

    if repo.is_dirty():
        path_to_readme = os.path.join(repo.working_tree_dir, "README.md")
        repo.index.add([path_to_readme])
        repo.index.commit("Update submission form url")
        print("--> commit README.md")

    remote_url = gitutils.create_repo_on_github(gh, repo_name, organization)
    print("--> create repo: " + remote_url)
    remote = repo.create_remote(organization, remote_url)
    remote.push(default_branch_name)
    print(f"--> push {default_branch_name}")

    for ref in repo.references:
        if "solution" in ref.name:
            solution_branch = ref.name[7:]
            repo.git.checkout("-b", solution_branch, ref.name)
            remote.push(solution_branch)
            print("--> push " + solution_branch)

    repo.git.checkout(default_branch_name)
    print(f"--> checkout {default_branch_name}")

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
        help="organization",
    )
    args = parser.parse_args()
    deploy_main_and_solution(args.repo, args.org)


if __name__ == "__main__":
    main()
