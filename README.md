# Sharit

[![codecov](https://codecov.io/gh/dsebastien/sharit/branch/main/graph/badge.svg?token=sharit_token_here)](https://codecov.io/gh/dsebastien/sharit)
[![CI](https://github.com/dsebastien/sharit/actions/workflows/main.yml/badge.svg)](https://github.com/dsebastien/sharit/actions/workflows/main.yml)

## Install it from PyPI

```bash
pip install sharit
```

## Usage

```bash
$ sharit --url <url_to_share> --twitter-api-key ... --twitter-api-secret-key ... --slack-webhook-url ... --sub-reddit ... --reddit-client-id  ... --reddit-secret ... --reddit-refresh-token ...
```

## Getting the API keys

### Reddit
- Go to https://www.reddit.com/prefs/apps
- Create an application
  - Set the name you want
  - Select type 'script'
  - Enter a description
  - Set the redirect uri to `http://localhost:8080` (will be used to retrieved the refresh token)
- Take note of the client id (below "personal use script") and secret
- Get a refresh token by running: `python ./utils/get-refresh-token.py --reddit-client-id <client id> --reddit-secret <secret>` and save it somewhere safe along with the client id and secret

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
