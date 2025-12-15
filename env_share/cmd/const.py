import os

ENVS = ["dev", "stg", "prd"]
ENV_DIR = ".env"
LATEST_DIR = os.path.join(ENV_DIR, "latest")
KEYS_DIR = os.path.join(ENV_DIR, "keys")
GITIGNORE_PATH = ".gitignore"
ENCRYPTED_PREFIX = "encrypted:"
ENC_DIR = "env_share"
TMP_DIR ="tmp"
WORK_DIR = os.path.join(TMP_DIR, "env_share")
GITIGNORE_REQUIRED = [f"{ENV_DIR}/*", f"{TMP_DIR}/*", "*.keys"]
