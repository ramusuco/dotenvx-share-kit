# dotenvx-share-kit

A toolkit for securely sharing `.env` files across your team using Git submodules and dotenvx encryption.

## Features

- **Git Submodule** - Embed into any project without polluting your codebase
- **VS Code Integration** - Run encryption/decryption from launch.json
- **Clean Separation** - Encrypted files live in parent project, not in submodule
- **Non-destructive** - Never overwrites your local plaintext `.env` files

## Requirements

- Python 3.11+
- [dotenvx](https://dotenvx.com/docs/install) 1.51.1+

## Installation

### 1. Clone to your repository root

```bash
git clone https://github.com/yourname/dotenvx-share-kit.git env_share
rm -rf env_share/.git
```

### 2. Copy sample launch.json to your repository root

```bash
mkdir -p .vscode
cp env_share/.vscode/launch.json.example .vscode/launch.json
```

Or add to your existing `.vscode/launch.json`:

```json
{
    "configurations": [
        {
            "name": "encrypt",
            "type": "debugpy",
            "request": "launch",
            "program": "env_share/scripts/encryption.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": { "PYTHONPATH": "${workspaceFolder}" }
        },
        {
            "name": "decrypt",
            "type": "debugpy",
            "request": "launch",
            "program": "env_share/scripts/decryption.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": { "PYTHONPATH": "${workspaceFolder}" }
        }
    ]
}
```

## Directory Structure

```
your-project/
├── .vscode/
│   └── launch.json
├── .env/
│   ├── dev                      # plaintext (gitignored)
│   ├── stg
│   ├── encrypted/               # encrypted files (tracked)
│   │   ├── .env.dev.enc
│   │   └── .env.stg.enc
│   ├── keys/                    # key files (gitignored)
│   │   └── dev.keys
│   └── latest/                  # decrypted output (gitignored)
│       └── .env.dev
└── env_share/                   # this submodule
```

## Usage

### Encrypt (first time)

1. Create plaintext file: `.env/dev`
2. Run `encrypt` in VS Code (or `python env_share/scripts/encryption.py dev`)
3. Share `.env/keys/dev.keys` with your team securely
4. Commit `.env/encrypted/.env.dev.enc`

### Add new keys

1. Add keys to `.env/dev`
2. Run `encrypt`
3. Commit updated `.env/encrypted/.env.dev.enc`

### Change existing values

1. Remove the key from `.env/encrypted/.env.dev.enc`
2. Update value in `.env/dev`
3. Run `encrypt`

### Decrypt

1. Place key file at `.env/keys/dev.keys`
2. Run `decrypt`
3. Output written to `.env/latest/.env.dev`

## Design Principles

- **Append-only** - Existing keys in `.enc` are never auto-overwritten
- **Non-destructive** - Decryption outputs to `latest/`, not your working `.env`
- **Explicit reset** - Delete `.enc` manually to regenerate

## Disclaimer

This repository is provided as-is. No warranty is provided; use at your own risk.

## References

- [dotenvx Documentation](https://dotenvx.com/docs/install)
