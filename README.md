## dotenvx Official Documentation
https://dotenvx.com/docs/install

## Tested Environment
- dotenvx: 1.51.1
- Python: 3.11

## Disclaimer
This repository is provided as-is. No warranty is provided; use at your own risk.

## Purpose
1. Use dotenvx more securely.
2. Get the latest env file quickly.
3. Ensure stable operation.
4. Use Python to minimize OS/environment differences.

## Design Philosophy
- This repo focuses only on safely sharing the latest env file; it never overwrites your local plain `.env/{env}`.
- By default, we only add new keys; existing keys in `.enc` are not overwritten. To change a value, delete the key from `.enc` and rerun encryption to add it back as a new key.
- Decryption writes to `.env/latest/.env.{env}` and does not overwrite your plain `.env/{env}`.
- Reset is explicit: delete the target `.enc` file manually, then rerun encryption to regenerate it with the existing key.

## Usage

### Encryption (first run)
1. Prepare the plain env file (e.g. `.env/dev`, `.env/stg`).
2. Run `env_share/bin/encryption.py {env}` (on the first run, this creates the key and `env_share/.env.{env}.enc`).
3. Share `.env/keys/{env}.keys` securely with your team (gitignored).

### Add new values (requires the key)
1. Update the plain env file (e.g. `.env/dev`, `.env/stg`).
2. Run `env_share/bin/encryption.py {env}`.
3. New keys are appended to `env_share/.env.{env}.enc`; commit/push as needed.

### Reset the encrypted file
1. Delete `env_share/.env.{env}.enc` for the target env.
2. Run `env_share/bin/encryption.py {env}` again to regenerate `.enc` with the existing key.

### Change existing values
1. Remove the target key from `env_share/.env.{env}.enc`.
2. Put the desired value in the plain `.env/{env}` and rerun `env_share/bin/encryption.py {env}`.

### Decryption
1. Place the key at `.env/keys/{env}.keys`.
2. Run `env_share/bin/decryption.py {env}`; decrypted output is written to `.env/latest/.env.{env}`.

---

## dotenvxの公式ドキュメント
https://dotenvx.com/docs/install

## 動作確認した環境
dotenvx : 1.51.1
Python  : 3.11

## 免責事項
自由に使用しても構いませんが、内容や動作は保証しません自己責任でお願いします。

## 目的
1. dotenvx をより安全に使う
2. 最新のenvをすぐに入手する
3. 安定動作を確保する
4. Python で OS 差分を減らす

## 設計思想
- 最新のenvファイルを安全に共有する事だけを目的とし、個人の平文 `.env/{env}` は上書きしない
- 基本は「新規キーの追加」を行い、`.enc` の既存キーは自動で上書きしない値を変えるときはencから削除して、再度新規キーとして追加
- 復号は `.env/latest/.env.{env}` へ出力し、個人の平文 `.env/{env}` は上書きしない
- リセットは明示的に手動で `.enc` を削除してから再生成

## 使い方

### 暗号化（初回）
1. 平文の env ファイルを用意（例: `.env/dev` や `.env/stg`）
2. `env_share/bin/encryption.py {env}` を実行（初回の暗号化で鍵と `env_share/.env.{env}.enc` が作成されます）
3. `.env/keys/{env}.keys` を安全な手段でチームに共有する（gitignore 済み）

### 新規の値を追加する（鍵がある前提）
1. 平文の env ファイルを更新する（例: `.env/dev` や `.env/stg`）
2. `env_share/bin/encryption.py {env}` を実行する
3. `env_share/.env.{env}.enc` に値が追加されるので必要に応じて push する

### 暗号化ファイルをリセットする
1. 対象環境の `env_share/.env.{env}.enc` を削除する
2. `env_share/bin/encryption.py {env}` を再実行する（既存の鍵で `.enc` を再生成します）

### 既存の値を変える
1. `env_share/.env.{env}.enc` から該当キーを削除する
2. 平文 `.env/{env}` に望む値を入れて `encryption.py` を再実行する

### 復号化
1. 対応する鍵を `.env/keys/{env}.keys` に置く
2. `env_share/bin/decryption.py {env}` を実行すると、復号結果が `.env/latest/.env.{env}` に書き出される
