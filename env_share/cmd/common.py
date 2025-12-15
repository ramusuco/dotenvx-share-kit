import os
import logging
import subprocess
from env_share.cmd.const import (
    GITIGNORE_PATH,
    ENCRYPTED_PREFIX,
    ENV_DIR,
    ENC_DIR,
    WORK_DIR,
    GITIGNORE_REQUIRED,
    KEYS_DIR,
    LATEST_DIR
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_kv_file(file_path: str) -> dict:
    kv_data: dict[str, str] = {}
    with open_file(file_path, 'r') as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith('#') or '=' not in s:
                continue
            key, value = s.split('=', 1)
            key = key.strip()
            value = value.strip()
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
    ensure_dirs([ENV_DIR, WORK_DIR, LATEST_DIR, ENC_DIR, KEYS_DIR])
    key_file = os.path.join(KEYS_DIR, f"{target_env}.keys")
    enc_file = os.path.join(ENC_DIR, f".env.{target_env}.enc")
    env_plain_file = os.path.join(ENV_DIR, target_env)
    env_latest_file = os.path.join(LATEST_DIR, f".env.{target_env}")
    work_enc_file = os.path.join(WORK_DIR, f".env.{target_env}.enc")
    return enc_file, env_plain_file, env_latest_file, work_enc_file, key_file


def ensure_encrypted_values(enc_file: str) -> None:
    with open_file(enc_file, "r") as f:
        for line in f:
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.strip().split("=", 1)
            if key.startswith("DOTENV_PUBLIC_KEY"):
                continue
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                value = value[1:-1]
            if not value.startswith(ENCRYPTED_PREFIX):
                raise RuntimeError(f"unencrypted value detected in {enc_file}: {line.strip()}")


def ensure_gitignore() -> None:
    required = GITIGNORE_REQUIRED
    if not os.path.isfile(GITIGNORE_PATH):
        raise FileNotFoundError(f".gitignore not found: {GITIGNORE_PATH}")

    with open_file(GITIGNORE_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    norm_lines = {line.rstrip("/") for line in lines}

    missing = []
    for entry in required:
        if entry.rstrip("/") not in norm_lines:
            missing.append(entry)

    if missing:
        raise RuntimeError(f".gitignore lacks entries: {', '.join(missing)}")

def open_file(
        path, 
        mode,
    ):
    if mode == 'w':
        return open(path, mode, encoding="utf-8", newline="")
    return open(path, mode, encoding="utf-8")