## official
https://dotenvx.com/docs/install

## Initialization

### If there are no encrypted files yet
1. Prepare env file
2. Run `env_share/cmd/encryption.py` and specify the env
3. Share .env/.env.{env}.keys with teammates

### If you have an encrypted file and want to reset it
1. Delete the .keys and .enc files for the environment you wish to initialize.
2. Run `env_share/cmd/encryption.py` and specify the env