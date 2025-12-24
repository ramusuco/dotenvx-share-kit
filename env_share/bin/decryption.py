import shutil
import logging
from env_share.config import *
from env_share.lib.paths import prepare_paths
from env_share.lib.dotenvx_runner import run_decrypt
from env_share.lib.validation import validate_files, ensure_gitignore, ensure_encrypted_values, validate_environment
from env_share.lib.io_utils import open_file, cleanup_tmp

logger = logging.getLogger(__name__)


def main(target_env: str) -> None:
    validate_environment(target_env)
    (
        enc_file,
        _,
        env_latest_file,
        work_enc_file,
        key_file
    ) = prepare_paths(target_env)

    ensure_gitignore()
    validate_files([key_file, enc_file])

    try:
        shutil.copy(enc_file, work_enc_file)

        run_decrypt(work_enc_file, key_file)
        write_without_header(work_enc_file, env_latest_file)
        logger.info(f"wrote {env_latest_file}")
    finally:
        cleanup_tmp([work_enc_file])
        ensure_encrypted_values(enc_file)


def write_without_header(
        work_enc_file: str,
        env_latest_file: str
) -> None:
    with open_file(work_enc_file, 'r') as src, open_file(env_latest_file, 'w') as out:
        started = False
        for line in src:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                if started:
                    out.write(line)
                continue
            if '=' not in line:
                if started:
                    out.write(line)
                continue
            key, _ = stripped.split('=', 1)
            if key.strip().startswith('DOTENV_'):
                continue
            if not started:
                started = True
            out.write(line)


if __name__ == "__main__":
    main(input("please enter target env: "))
