# Sharit

[![codecov](https://codecov.io/gh/dsebastien/sharit/branch/main/graph/badge.svg?token=sharit_token_here)](https://codecov.io/gh/dsebastien/sharit)
[![CI](https://github.com/dsebastien/sharit/actions/workflows/main.yml/badge.svg)](https://github.com/dsebastien/sharit/actions/workflows/main.yml)

## Install it from PyPI

```bash
pip install sharit
```

## Usage

```bash
$ sharit --url <url_to_share> --twitter-api-key ... --twitter-api-secret-key ... --twitter-access-token ... --twitter-access-token-secret ... --sub-reddit ... --reddit-client-id  ... --reddit-secret ... --reddit-refresh-token ... --slack-bot-token= ... --slack-channel "#..."
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

### Slack
- Go to https://api.slack.com/apps?new_app=1
- Create an app using a template and use the following JSON config

```json
{
    "display_information": {
        "name": "Sharit",
        "description": "Bot that shares links for the community"
    },
    "features": {
        "bot_user": {
			"display_name": "SharitBot",
			"always_online": true
		},
		"app_home": {
			"home_tab_enabled": false,
			"messages_tab_enabled": false
		}
    },
    "oauth_config": {
		"scopes": {
			"bot": [
				"chat:write",
				"chat:write.public"
			]
		}
	},
    "settings": {
        "org_deploy_enabled": false,
        "socket_mode_enabled": false,
        "is_hosted": false,
        "token_rotation_enabled": false
    }
}
```

Then:
- Install the newly created bot in the workspace you want to be able to send links to
- Once done, go to "OAuth & Permissions" and take note of the Bot User OAuth Token

### Twitter
- Go to https://developer.twitter.com/
- Create a developer account
- Make sure that your application has read/write access by going to the app > User authentication settings > User authentication set up Edit. App permissions should be set to Read and write (at least)
- Edit the default application to get the secrets under "Keys and tokens"

Note that the API key and API key secret correspond to the consumer key and consumer secret).

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
