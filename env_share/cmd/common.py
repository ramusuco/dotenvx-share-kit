import os
import logging
import subprocess
from env_share.cmd.const import (
    KEY_PATH,
    GITIGNORE_PATH,
    ENCRYPTED_PREFIX,
    ENV_DIR,
    ENC_DIR,
    TMP_DIR,
    GITIGNORE_REQUIRED,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_kv_file(file_path: str) -> dict:
    kv_data: dict[str, str] = {}
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith('#') or '=' not in s:
                continue
            key, value = s.split('=', 1)
            kv_data[key] = value
    return kv_data

load_env_file = load_kv_file
load_enc_file = load_kv_file

def run_decrypt(enc_file: str, key_path: str) -> None:
    try:
        subprocess.run(
            ["dotenvx", "decrypt", "-fk", key_path, "-f", enc_file],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        stderr = e.stderr
        if isinstance(stderr, bytes):
            stderr = stderr.decode('utf-8', errors='replace')
        logger.error(f"decrypt failed: {stderr}")
        raise

def run_encrypt(plain_file: str, key_path: str) -> None:
    try:
        subprocess.run(
            ["dotenvx", "encrypt", "-fk", key_path, "-f", plain_file],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        stderr = e.stderr
        if isinstance(stderr, bytes):
            stderr = stderr.decode('utf-8', errors='replace')
        logger.error(f"encrypt failed: {stderr}")
        raise

def validate_files(files: list[str]) -> None:
    for file_path in files:
        file_existence_confirmation(file_path)

def file_existence_confirmation(file_path: str) -> None:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    logger.info(f"File exists: {file_path}")

def cleanup_tmp(paths) -> None:
    for file_path in paths:
        if os.path.isfile(file_path):
            os.remove(file_path)

def ensure_dirs(dirs) -> None:
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def prepare_paths(target_env: str):
    env_dir = ENV_DIR
    tmp_dir = TMP_DIR
    enc_dir = ENC_DIR
    ensure_dirs([tmp_dir, env_dir, enc_dir])

    # per-environment key file (e.g. .env/.dev.keys)
    key_file = os.path.join(env_dir, f".{target_env}.keys")
    enc_file = os.path.join(enc_dir, f".env.{target_env}.enc")
    env_plain_file = os.path.join(env_dir, target_env)
    env_latest_file = os.path.join(env_dir, f"{target_env}_latest")
    work_enc_file = os.path.join(tmp_dir, f".env.{target_env}.enc")
    return enc_file, env_plain_file, env_latest_file, work_enc_file, key_file

def ensure_encrypted_values(enc_file: str) -> None:
    with open(enc_file, "r") as f:
        for line in f:
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.strip().split("=", 1)
            if key.startswith("DOTENV_PUBLIC_KEY"):
                continue
            if not value.startswith(ENCRYPTED_PREFIX):
                raise RuntimeError(f"unencrypted value detected in {enc_file}: {line.strip()}")

def ensure_gitignore() -> None:
    required = GITIGNORE_REQUIRED
    if not os.path.isfile(GITIGNORE_PATH):
        raise FileNotFoundError(f".gitignore not found: {GITIGNORE_PATH}")

    with open(GITIGNORE_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    norm_lines = {line.rstrip("/") for line in lines}

    missing = []
    for entry in required:
        if entry.rstrip("/") not in norm_lines:
            missing.append(entry)

    if missing:
        raise RuntimeError(f".gitignore lacks entries: {', '.join(missing)}")
