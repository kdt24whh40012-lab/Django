# Git 手順
## 初期化
git init

## ユーザー設定(Githubのユーザー名とメールアドレス)
git config --local user.name "自分の名前"
git config --local user.email "自分のemail"

## 確認(ユーザ名とアドレス)
git config -l

## 除外ファイル(.gitignore)
```
.venv/*
*/__pycache__/*
```

## requirements.txt
```
pip freeze > requirements.txt
```

## 初回コミット
```
git add .
git commit -m "初回コミット"
```

## Git Clone
githubから最新のリポジトリを取得

```
git clone [リポジトリのURL]