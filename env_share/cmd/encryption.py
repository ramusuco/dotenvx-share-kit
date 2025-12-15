import os
import sys      
import shutil
import logging
from env_share.cmd.const import *
from env_share.cmd.common import *

logger = logging.getLogger(__name__)

def main(target_env: str) -> None:
    enc_file, env_file, _, work_enc, key_file = prepare_paths(target_env)
    ensure_gitignore()
    created_new_enc = ensure_encrypted_file_exists(enc_file)

    if not created_new_enc:
        validate_files([key_file, enc_file, env_file])
    else:
        validate_files([enc_file, env_file])

    try:
        if created_new_enc:
            shutil.copy(env_file, work_enc)
        else:
            shutil.copy(enc_file, work_enc)
            run_decrypt(work_enc, key_file)

        updated = True if created_new_enc else embed_difference(env_file, work_enc)
        if not updated:
            logger.info("No missing keys. Skipped re-encrypt.")
            return

        run_encrypt(work_enc, key_file)
        ensure_encrypted_values(work_enc)
        shutil.move(work_enc, enc_file)
        logger.info("Updated encrypted env file.")
    finally:
        cleanup_tmp([work_enc])
        ensure_encrypted_values(enc_file)


def embed_difference(env_file: str, work_enc_file: str) -> bool:
    load_env_data = load_env_file(env_file)
    load_work_enc_data = load_enc_file(work_enc_file)
    add_data = {k: v for k, v in load_env_data.items() if k not in load_work_enc_data}
    if not add_data:
        logger.warning("New keys is not found.")
        return False
    add_data_to_plain_file(add_data, work_enc_file)
    return True


def add_data_to_plain_file(add_data: dict, plain_file: str) -> None:
    with open_file(plain_file, 'a') as f:
        for key, value in add_data.items():
            f.write(f"{key}={value}\n")
            logger.info(f"【NEW KEY】: {key}")


def ensure_encrypted_file_exists(enc_file: str) -> bool:
    if os.path.isfile(enc_file):
        return False
    with open_file(enc_file, 'w'):
        pass
    logger.info(f"created empty encrypted env file: {enc_file}")
    return True

if __name__ == "__main__":
    main(input("please enter target env: "))
