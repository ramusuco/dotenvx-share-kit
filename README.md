## Official
https://dotenvx.com/docs/install

## Requirements
- dotenvx 1.51.1
- Python 3.11

## Disclaimer
You may use this repository freely, but it is provided "as is" without warranty; the author is not responsible for any damages.

## Purpose
1. Use dotenvx more securely.
2. Share only the common env vars while letting each developer keep personal settings locally.
3. Ensure stable operation.
4. Use Python to minimize OS/environment differences.

## Design philosophy
- Shared values live in encrypted files; personal/local settings stay in plain `.env/{env}`.
- Operations are additive: existing keys in `.enc` are not overwritten automatically; delete a key intentionally before changing it.
- Decryption writes to `.env/latest/.env.{env}` and does not touch your plain `.env/{env}`.
- Resetting is explicit: delete the `.enc` file if you want to rebuild it with the existing key.

## Usage

### Encryption (first run)
1. Prepare the plain env file (e.g. `.env/dev`, `.env/stg`).
2. Run `env_share/bin/encryption.py {env}` (first run creates the key and `env_share/.env.{env}.enc`).
3. Share `.env/keys/{env}.keys` securely with teammates (gitignored).

### Add new values (requires the key)
1. Update the plain env file (e.g. `.env/dev`, `.env/stg`).
2. Run `env_share/bin/encryption.py {env}`.
3. The new keys are added to `env_share/.env.{env}.enc`; commit/push as needed.

### Reset the encrypted file
1. Delete `env_share/.env.{env}.enc` for that env.
2. Run `env_share/bin/encryption.py {env}` to regenerate `.enc` with the existing key.

### Change existing values
1. Remove the target key from `env_share/.env.{env}.enc`.
2. Put the desired value in the plain `.env/{env}` and rerun `env_share/bin/encryption.py`.

### Decryption
1. Place the key at `.env/keys/{env}.keys`.
2. Run `env_share/bin/decryption.py {env}`; output goes to `.env/latest/.env.{env}`.

---

## 公式ドキュメント
https://dotenvx.com/docs/install

## 動作環境
dotenvx : 1.51.1
Python  : 3.11

## 免責事項
自由に使用しても構いませんが、内容や動作は保証しません。自己責任でお願いします。

## 目的
1. dotenvx をより安全に使う。
2. 共有が必要な環境変数だけを揃え、個人設定は自由にできるようにする。
3. 安定動作を確保する。
4. Python で OS 差分を減らす。

## 設計思想
- 共有する値は暗号化ファイルに集約し、個人設定は平文 `.env/{env}` は触れない
- 基本は「新規キーの追加のみ」を行い、`.enc` の既存キーは自動で上書きしない。値を変えるときはencから削除して、再度暗号化して追加
- 復号は `.env/latest/.env.{env}` へ出力し、平文 `.env/{env}` は触れない
- リセットは明示的に `.enc` を削除してから再生成

## 使い方

### 暗号化（初回）
1. 平文の env ファイルを用意（例: `.env/dev` や `.env/stg`）。
2. `env_share/bin/encryption.py {env}` を実行（初回の暗号化で鍵と `env_share/.env.{env}.enc` が作成されます）。
3. `.env/keys/{env}.keys` を安全な手段でチームに共有する（gitignore 済み）。

### 新規の値を追加する（鍵がある前提）
1. 平文の env ファイルを更新する（例: `.env/dev` や `.env/stg`）。
2. `env_share/bin/encryption.py {env}` を実行する。
3. `env_share/.env.{env}.enc` に値が追加されるので必要に応じて push する。

### 暗号化ファイルをリセットする
1. 対象環境の `env_share/.env.{env}.enc` を削除する。
2. `env_share/bin/encryption.py {env}` を再実行する（既存の鍵で `.enc` を再生成します）。

### 既存の値を変える
1. `env_share/.env.{env}.enc` から該当キーを削除する。
2. 平文 `.env/{env}` に望む値を入れて `encryption.py` を再実行する。

### 復号化
1. 対応する鍵を `.env/keys/{env}.keys` に置く。
2. `env_share/bin/decryption.py {env}` を実行すると、復号結果が `.env/latest/.env.{env}` に書き出される。
