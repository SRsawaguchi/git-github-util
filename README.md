# git-github-util
よく行うGitやGitHubの操作を自動化するスクリプト。  
大量のリポジトリを作成する必要がある場合などに使う。  
※自分用  

## 以下の環境変数が設定されている前提

| Key | Value | 
| -- | -- |
| GITHUB_TOKEN | GitHubのアクセストークン |

## 依存関係のインストール

```
pip3 install -r requirements.txt
```

## deploy_main_and_solution.py
指定したパスにあるディレクトリを走査する。  
その中で、Gitのリポジトリであるものに以下の操作を行う。  

1. ブランチ名を`main`に変更(masterブランチなどにいる前提)
1. もし、`README.md`に変更がある場合、`commit`する。
1. 当該ディレクトリと同じ名前のリポジトリをGitHub上に作成。
1. 作成したURLに`main`を`push`する。
1. `solution`という名前のブランチがある場合、これも作成したリポジトリに`push`する。(複数ある場合、複数`push`する。)
1. `main`に`checkout`する。

## repo_urls.py
指定したOrganizationのリポジトリのURL一覧を表示する。

```
python3 repo_urls.py <organization>
```

## clone_all_branch.py
cloneする際、全てのリモートブランチをcloneする。  

パラメタ  
- `--url` 必須: cloneするリポジトリのURL
- `--dest` 必須: 保存するディレクトリを指定。（その中にcloneしたディレクトリが生成される。）

実行例
```
python3 clone_all_branch.py --url https://***.git --dest ./test
```

## deploy_repo.py
新規にGitHubにリポジトリを作成し、指定したローカルリポジトリの全てのブランチをPUSHする。  

パラメタ
- `--path` 必須: ローカルリポジトリのpath
- `--org` 必須: organization
- `--remote` 必須: 新規にGitHubに作成したremoteの名前

実行例
```
python3 deploy_repo.py --org some-org --remote some-org --path ./some/awesome-lib
```
