import os
from dataclasses import dataclass
from env_share.config import ENV_DIR, ENC_DIR, WORK_DIR, KEYS_DIR, LATEST_DIR
from env_share.lib.io_utils import ensure_dirs


@dataclass(frozen=True)
class EnvPaths:
    enc: str
    plain: str
    latest: str
    work: str
    key: str


def prepare_paths(target_env: str) -> EnvPaths:
    ensure_dirs([ENV_DIR, WORK_DIR, LATEST_DIR, ENC_DIR, KEYS_DIR])
    return EnvPaths(
        enc=os.path.join(ENC_DIR, f".env.{target_env}.enc"),
        plain=os.path.join(ENV_DIR, target_env),
        latest=os.path.join(LATEST_DIR, f".env.{target_env}"),
        work=os.path.join(WORK_DIR, f".env.{target_env}.enc"),
        key=os.path.join(KEYS_DIR, f"{target_env}.keys"),
    )
