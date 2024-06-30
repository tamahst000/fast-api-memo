# fast-api-memo

## 準備

1. リポジトリのクローン

```
git clone https://github.com/tamahst000/fast-api-memo.git
cd fast-api-memo
```

2. パッケージのインストール (pip か poetry どちらか好きな方を選択)

- pip

```
pip install -r requirements.txt
```

- poetry

```
poetry install --no-root
```

## アプリケーションの実行

1. FastAPI の起動

- pip

```
uvicorn py.endpoints:app --reload --port 8888
```

- poetry

```
poetry run uvicorn py.endpoints:app --reload --port 8888
```

2. エンドポイントにアクセス

- http://127.0.0.1:8888 にアクセスすればアプリケーションを操作できる

## データベース

SQLite3 を使用 ※Mac の場合は標準で sqlite が入っているが、windows の場合は別にインストールする必要がある

### データベースの新規作成

- pip

```
python create_table.py
```

- poetry

```
poetry run python create_table.py
```

`db.sqlite3`が作成される

### データベースを直接確認する

sqlite3 の起動

```
sqlite3 db.sqlite3
```

テーブルを確認

```
sqlite> .table
```

テーブルの中身を確認

```
sqlite> select * from user;

sqlite> select * from task;
```

sqlite3 の終了

```
sqlite> .q
```

## JSON レスポンス

### 保存されている全ユーザを取得

```
http://127.0.0.1:8888/get-user
```

### ユーザごとに保存されているメモを取得

```
http://127.0.0.1:8888/get-task/{username}
```

### ユーザを消去

```
http://127.0.0.1:8888/delete-user/{username}
```
