import argparse
import git
import os
import shutil
import sys


def create_new_repo_from(source_repo_path, dest_dir, src_dirs=None, exclude_dirs=None):
    """
    リポジトリをクローンし、新しいリポジトリを設定する

    Args:
        source_repo_path (str): ソースリポジトリのパス
        dest_dir (str): 出力先ディレクトリ
        src_dirs (list): solutionブランチにコピーするディレクトリのリスト
        exclude_dirs (list): 除外するディレクトリのリスト
    """
    print(f"\ncreating new repository from: {source_repo_path}")
    if not os.path.exists(source_repo_path):
        print(f"there is no source repository: {source_repo_path}")
        sys.exit(1)

    # ソースリポジトリの名前を取得
    repo_name = os.path.basename(source_repo_path)
    dest_repo_path = os.path.join(dest_dir, repo_name)

    # 出力先ディレクトリが存在するか確認
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # 出力先に同名のリポジトリが存在する場合は削除
    if os.path.exists(dest_repo_path):
        print(f"there is already a repository: {dest_repo_path}")
        sys.exit(1)

    # ディレクトリのコピー
    print(f"--> copying directory: {source_repo_path} -> {dest_repo_path}")
    shutil.copytree(
        source_repo_path, dest_repo_path, ignore=shutil.ignore_patterns(".git")
    )

    # 不要なディレクトリを削除
    print("--> removing unnecessary directories...")
    if exclude_dirs:
        for exclude_dir in exclude_dirs:
            exclude_path = os.path.join(dest_repo_path, exclude_dir)
            if os.path.exists(exclude_path):
                print(f"  - removing: {exclude_dir}")
                if os.path.isdir(exclude_path):
                    shutil.rmtree(exclude_path)
                else:
                    os.remove(exclude_path)

    # Gitの初期化
    print(f"--> initializing git repository: {dest_repo_path}")
    repo = git.Repo.init(dest_repo_path)

    # 最初のコミット
    repo.git.add(".")
    print("  - git add .")
    repo.git.commit("-m", "initial commit")
    print("  - commit created: 'initial commit'")

    # solutionブランチを作成
    print(f"--> setting up solution branch: {dest_repo_path}")
    repo.git.checkout("-b", "solution")
    print("  - 'solution' branch created")

    # solutionブランチの内容を更新
    if src_dirs:
        source_repo = git.Repo(source_repo_path)

        # すべてのリモートブランチをフェッチ
        print(f"  - fetching remote branches: {source_repo_path}")
        source_repo.git.fetch("--all")

        # コピー元リポジトリでsolutionブランチが存在する場合はチェックアウト
        solution_exists = False
        for ref in source_repo.references:
            if ref.name == "solution" or ref.name == "origin/solution":
                solution_exists = True
                source_repo.git.checkout("solution")
                break

        # 指定されたディレクトリをコピー
        print("  - copying directories to solution branch")
        for src_dir in src_dirs:
            source_path = os.path.join(source_repo_path, src_dir)
            dest_path = os.path.join(dest_repo_path, src_dir)

            if os.path.exists(source_path):
                print(f"    - copying: {src_dir} -> {dest_path}")
                if os.path.exists(dest_path):
                    if os.path.isdir(dest_path):
                        shutil.rmtree(dest_path)
                    else:
                        os.remove(dest_path)

                if os.path.isdir(source_path):
                    shutil.copytree(source_path, dest_path)
                else:
                    shutil.copy2(source_path, dest_path)
            else:
                print(f"    - warning: source directory does not exist: {source_path}")

        # 元のリポジトリをmainブランチに戻す（必要に応じて）
        if solution_exists:
            source_repo.git.checkout("main")
            print(f"  - checkout to main branch: {source_repo_path}")

        # コミット
        print(f"  - committing changes to solution branch: {dest_repo_path}")
        repo.git.add(".")
        print("    - git add .")
        repo.git.commit("-m", "solution")
        print("    - commit created: 'initial commit'")

    # mainブランチに戻る
    repo.git.checkout("main")
    print(f"--> checkout to main branch: {dest_repo_path}")
    print(f"--> completed! new repository created: {dest_repo_path}")

    return dest_repo_path


def push_to_github(repo_path, organization):
    """
    GitHubにリポジトリをプッシュする

    Args:
        repo_path (str): リポジトリのパス
        organization (str): GitHubの組織名
    """
    try:
        import gitutils
    except ImportError:
        print(
            "警告: gitutilsモジュールがインポートできません。GitHubへのプッシュ機能は無効です。"
        )
        return

    repo = git.Repo(repo_path)
    repo_name = os.path.basename(repo_path)

    print(f"--> setting up GitHub repository: {organization}/{repo_name}")
    try:
        # GitHubのインスタンスを取得
        gh = gitutils.get_github()

        # GitHubにリポジトリを作成
        remote_url = gitutils.create_repo_on_github(gh, repo_name, organization)
        print(f"  - created repository: {remote_url}")

        # リモートを追加
        remote = repo.create_remote("origin", remote_url)
        print(f"  - added remote: {remote_url}")

        # mainブランチをプッシュ
        remote.push("main")
        print(f"  - pushed main branch")

        # solutionブランチをプッシュ
        remote.push("solution")
        print(f"  - pushed solution branch")

        print(
            f"*** completed! repository pushed to GitHub: https://github.com/{organization}/{repo_name} ***"
        )
    except Exception as e:
        print(f"エラー: GitHubへのプッシュに失敗しました: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="リポジトリのクローンと複製を行うスクリプト"
    )
    parser.add_argument("--repo", required=True, help="元となるリポジトリのパス")
    parser.add_argument("--dest", required=True, help="出力先ディレクトリ")
    parser.add_argument(
        "--src",
        nargs="+",
        default=["src"],
        help="solutionブランチにコピーするディレクトリ（複数指定可）",
    )
    parser.add_argument(
        "--exclude", nargs="+", default=[], help="除外するディレクトリ（複数指定可）"
    )
    parser.add_argument("--org", help="GitHubの組織名（プッシュする場合）")

    args = parser.parse_args()

    # リポジトリのクローンと設定
    repo_path = create_new_repo_from(args.repo, args.dest, args.src, args.exclude)

    # GitHubにプッシュ（組織名が指定されている場合）
    if args.org:
        push_to_github(repo_path, args.org)
    else:
        print(
            "注意: --orgオプションが指定されていないため、GitHubへのプッシュは行いません。"
        )


if __name__ == "__main__":
    main()
