import os
from env_share.config import ENV_DIR, ENC_DIR, WORK_DIR, KEYS_DIR, LATEST_DIR
from env_share.lib.io_utils import ensure_dirs


def prepare_paths(target_env: str) -> tuple[str, str, str, str, str]:
    ensure_dirs([ENV_DIR, WORK_DIR, LATEST_DIR, ENC_DIR, KEYS_DIR])
    key_file = os.path.join(KEYS_DIR, f"{target_env}.keys")
    enc_file = os.path.join(ENC_DIR, f".env.{target_env}.enc")
    env_plain_file = os.path.join(ENV_DIR, target_env)
    env_latest_file = os.path.join(LATEST_DIR, f".env.{target_env}")
    work_enc_file = os.path.join(WORK_DIR, f".env.{target_env}.enc")
    return enc_file, env_plain_file, env_latest_file, work_enc_file, key_file
