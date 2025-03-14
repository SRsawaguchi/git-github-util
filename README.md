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
指定したローカルのリポジトリについて以下の操作を行う。  

1. ブランチ名を`main`に変更(masterブランチなどにいる前提)
1. もし、`README.md`に変更がある場合、`commit`する。
1. 当該ディレクトリと同じ名前のリポジトリをGitHub上に作成。
1. 作成したURLに`main`を`push`する。
1. `solution`という名前のブランチがある場合、これも作成したリポジトリに`push`する。(複数ある場合、複数`push`する。)
1. `main`に`checkout`する。
1. branch protection ruleを追加する。(mainブランチへのマージにPRへのApproveを必須にする。)

パラメタ
- `--repo` 必須: リポジトリへのpath
- `--org` 必須: organization
- `--branch-protection` 任意: Trueを指定するとブランチプロテクションを設定する。デフォルトはFalse。

実行例
```
python3 deploy_main_and_solution.py --repo ./path/to/repo --org some-org
```

## add_branch_protection.py
指定したリポジトリにブランチプロテクションを設定する。  
ブランチプロテクションの内容は、指定したブランチへのマージにApproveを必須とするもの。


パラメタ
- `--repo` 必須: リポジトリ名
- `--org` 必須: organization
- `--branch` 任意: protectionするブランチ。デフォルトは`main`。

実行例
```
python3 add_branch_protection.py --org some-org --repo some_repo --branch develop
```

## repo_urls.py
指定したOrganizationのリポジトリのURL一覧を表示する。

```
python3 repo_urls.py --org <organization> --hostname <hostname>
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
- `--prefix`: github上に作成するリポジトリのprefix

実行例
```
python3 deploy_repo.py --org some-org --remote some-org --path ./some/awesome-lib
```

## deploy_branch.py
指定したブランチを指定したURLのリモートリポジトリにpushする。  

パラメタ
- `--path` 必須: ローカルリポジトリのpath
- `--url` 必須: リモートのURL
- `--branch` 必須: pushするブランチ名

※`ad9055f94eb34ad2-90ccd5811527bc6e`という名前の一時remoteを作成します。（処理がおわったら自動でremoveする。）

実行例
```
python3 deploy_branch.py --url https://*** --branch feature --path ./some/awesome-lib
```

## create_new_repo_from.py
とあるリポジトリを元に、新しいリポジトリを作成できます。以下が可能です。  
- 指定したディレクトリ（リポジトリ）をcopyして新しいリポジトリを作成（除外するフォルダを指定できます。）
- 元のリポジトリのsolutionブランチにある変更を新しいリポジトリのsolutionブランチとして作成（反映させるフォルダを選択可能）
- 指定したGitHub Organizationへのリポジトリの作成およびpush

なお、新しいリポジトリには、元のリポジトリの履歴は引き継がれません。

パラメタ
- `--repo` 必須: 元となるリポジトリのパス
- `--dest` 必須: 出力先ディレクトリ
- `--src` 任意: solutionブランチにコピーするディレクトリ (複数指定可)。デフォルトは"src"
- `--exclude` 任意: 除外するディレクトリ (複数指定可)
- `--org` 任意: GitHubの組織名 (プッシュする場合)

実行例
```
python3 create_new_repo_from.py \
    --org some-org \
    --repo ../repos/_transfer/course.web0x.work_html \
    --dest ../repos/web \
    --src src \
    --exclude ai_tool .github
```

この例では:
1. `../repos/_transfer/course.web0x.work_html` リポジトリをコピーして `../repos/web` に新しいリポジトリを作成(このとき、ai_toolsと.githubフォルダは新しいリポジトリにコピーされません。)
2. 新しいリポジトリのgitを初期化し、コピーした内容でmainブランチを作成
3. 元のリポジトリの`solution`ブランチにある`src` ディレクトリを新しいリポジトリにコピーし、この状態で`solution`ブランチを作成。
5. 作成したリポジトリを `some-org` 組織にプッシュ
