## official
https://dotenvx.com/docs/install

## Purpose

1. Use dotenvx more securely.
2. Make it easier to use with the VS Code debugger.
3. Ensure stable operation.
4. Use Python to minimize environment-to-environment differences when running the helper scripts.

## Initialization

### If there are no encrypted files yet
1. Prepare env file (e.g. `.env/dev` or `.env/stg`).
2. Run `env_share/cmd/encryption.py` and specify the env.
3. Share `.env/.env.{env}.keys` with teammates via a secure channel (these files are gitignored).

### If you have an encrypted file and want to reset it
1. Delete the .keys and .enc files for the environment you wish to initialize.
2. Run `env_share/cmd/encryption.py` and specify the env.

### Notes
- Install dotenvx beforehand (see official docs above).
- For debugging in VS Code, you can point `envFile` to your plain `.env/{env}` during local runs.
- Existing keys in `.env.{env}.enc` are not updated when their values change in plain `.env/{env}`. If you need to change a value, remove the key from the encrypted file and rerun `env_share/cmd/encryption.py`.
