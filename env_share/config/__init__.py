import os

PROJECT_NAME = "env_share"

ENVS = ["dev", "stg", "prd"]
ENV_DIR = ".env"
LATEST_DIR = os.path.join(ENV_DIR, "latest")
KEYS_DIR = os.path.join(ENV_DIR, "keys")
GITIGNORE_PATH = ".gitignore"
ENCRYPTED_PREFIX = "encrypted:"
ENC_DIR = os.path.join(PROJECT_NAME, "encrypted")
TMP_DIR = "tmp"
WORK_DIR = os.path.join(TMP_DIR, PROJECT_NAME)

IGNORE_WORK_DIR = f"{TMP_DIR}/{PROJECT_NAME}"
GITIGNORE_REQUIRED = [f"{ENV_DIR}/*", f"{IGNORE_WORK_DIR}/*", "*.keys"]
