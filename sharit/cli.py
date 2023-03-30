import argparse
import json
import os
import requests
import sys
import validators

"""CLI interface
"""

def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m sharit` and `$ sharit `.
    """

    program_name="Sharit"
    program_description="Share links with multiple targets"

    # Get current version
    version_file = open('./sharit/VERSION','r')
    program_version = version_file.readline()
    version_file.close()

    print("Welcome to {program} {version}".format(program=program_name, version=program_version))

    parser = argparse.ArgumentParser(
      prog=program_name,
      description=program_description,
      epilog="Thanks for using %(prog)s! :)",
    )

    parser.add_argument("-u", "--url", required=True)
    parser.add_argument("-rat", "--reddit-access-token", required=True)
    parser.add_argument("-tak", "--twitter-api-key", required=True)
    parser.add_argument("-task", "--twitter-api-secret-key", required=True)
    parser.add_argument("-swu", "--slack-webhook-url", required=True)

    args = parser.parse_args()

    if not validators.url(args.url):
      sys.exit('Invalid URL')

    if not args.reddit_access_token:
      sys.exit("Invalid Reddit access token")

    if not args.twitter_api_key:
      sys.exit("Invalid Twitter API key")

    if not args.twitter_api_secret_key:
      sys.exit("Invalid Twitter API secret key")

    if not validators.url(args.slack_webhook_url):
      sys.exit("Invalid Slack Webhook URL")

    url_to_share=args.url

    # Set up credentials for different APIs
    REDDIT_ACCESS_TOKEN = args.reddit_access_token
    TWITTER_API_KEY = args.twitter_api_key
    TWITTER_API_SECRET_KEY = args.twitter_api_secret_key
    SLACK_WEBHOOK_URL = args.slack_webhook_url

    print(url_to_share)
    print(REDDIT_ACCESS_TOKEN)
    print(TWITTER_API_KEY)
    print(TWITTER_API_SECRET_KEY)
    print(SLACK_WEBHOOK_URL)

