# dotenvx-share-kit

Git サブモジュールとして組み込み、チームで `.env` を安全に共有するためのツールキット。

## 特徴

- **サブモジュールとして動作** - 親プロジェクトに組み込んで使用
- **VS Code launch.json から実行** - デバッグ設定で簡単に暗号化/復号化
- **暗号化ファイルは親プロジェクト側に生成** - サブモジュール内は常にクリーン
- **平文を上書きしない** - 個人の `.env/{env}` は安全

## 動作確認環境

- dotenvx: 1.51.1
- Python: 3.11

## セットアップ

### 1. サブモジュールとして追加

```bash
git submodule add https://github.com/yourname/dotenvx-share-kit.git env_share
```

### 2. launch.json を親プロジェクトにコピー

```bash
cp env_share/.vscode/launch.json .vscode/
```

または既存の launch.json に以下を追加:

```json
{
    "configurations": [
        {
            "name": "encrypt",
            "type": "debugpy",
            "request": "launch",
            "program": "env_share/scripts/encryption.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": { "PYTHONPATH": "${workspaceFolder}" }
        },
        {
            "name": "decrypt",
            "type": "debugpy",
            "request": "launch",
            "program": "env_share/scripts/decryption.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": { "PYTHONPATH": "${workspaceFolder}" }
        }
    ]
}
```

### 3. dotenvx をインストール

https://dotenvx.com/docs/install

## ディレクトリ構造

```
your-project/
├── .vscode/
│   └── launch.json
├── .env/
│   ├── dev                          # 平文 (gitignore)
│   ├── stg
│   ├── encrypted/                   # 暗号化ファイル (git管理)
│   │   ├── .env.dev.enc
│   │   └── .env.stg.enc
│   ├── keys/                        # 鍵ファイル (gitignore)
│   │   └── dev.keys
│   └── latest/                      # 復号結果 (gitignore)
│       └── .env.dev
└── env_share/                       # このサブモジュール
    ├── scripts/
    │   ├── encryption.py
    │   └── decryption.py
    └── ...
```

## 使い方

### 暗号化（初回）

1. 平文ファイルを用意: `.env/dev`
2. VS Code で `encrypt` を実行（または `python env_share/scripts/encryption.py dev`）
3. 初回実行で `.env/keys/dev.keys` と `.env/encrypted/.env.dev.enc` が生成
4. `.keys` ファイルを安全な手段でチームに共有

### 新規キーの追加

1. 平文 `.env/dev` に新しいキーを追加
2. `encrypt` を実行
3. `.env/encrypted/.env.dev.enc` に追記される → commit/push

### 既存の値を変更

1. `.env/encrypted/.env.dev.enc` から該当キーを削除
2. 平文に新しい値を入れて `encrypt` を実行

### 復号化

1. `.env/keys/dev.keys` を配置
2. `decrypt` を実行
3. `.env/latest/.env.dev` に出力される

## 設計思想

- **追加のみ、上書きなし** - 既存キーは自動上書きしない
- **平文は触らない** - 復号結果は `latest/` に出力
- **リセットは明示的** - `.enc` を手動削除して再生成

## 免責事項

This repository is provided as-is. No warranty is provided; use at your own risk.

## 参考

- [dotenvx 公式ドキュメント](https://dotenvx.com/docs/install)
