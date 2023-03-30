# Sharit

[![codecov](https://codecov.io/gh/dsebastien/sharit/branch/main/graph/badge.svg?token=sharit_token_here)](https://codecov.io/gh/dsebastien/sharit)
[![CI](https://github.com/dsebastien/sharit/actions/workflows/main.yml/badge.svg)](https://github.com/dsebastien/sharit/actions/workflows/main.yml)

## Install it from PyPI

```bash
pip install sharit
```

## Usage

```bash
" sharit --url <url_to_share> --twitter-api-key ... --twitter-api-secret-key ... --slack-webhook-url ... --sub-reddit ... --reddit-client-id  ... --reddit-secret ... --reddit-username ... --reddit-password ...
```

Note that if 2FA is enabled on your Reddit account, you have to pass the password with the following form: `--reddit-password <username>:<second factor>`

## Getting the API keys

### Reddit
- Go to https://www.reddit.com/prefs/apps
- Create an application
  - Set the name you want
  - Select type 'script'
  - Enter a description
  - Set the redirect uri to `http://localhost:8080` (won't be used anyway)
- Take note of the client id (below "personal use script") and secret

Reference: https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
