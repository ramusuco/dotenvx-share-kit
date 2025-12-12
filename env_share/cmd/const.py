import os

ENVS = ["dev", "stg", "prd"]
ENV_DIR = ".env"
GITIGNORE_PATH = ".gitignore"
ENCRYPTED_PREFIX = "encrypted:"
ENC_DIR = "env_share"
TMP_DIR = os.path.join("tmp", "env_share")
GITIGNORE_REQUIRED = [f"{ENV_DIR}/*", TMP_DIR.replace(os.sep, '/') + "/*"]
