import argparse
import json
import os
import praw
import requests
import sys
import validators
import lxml.html
import urllib.request as urllib

"""CLI interface
"""

program_name="Sharit"
program_description="Share links with multiple targets"

# Get current version
version_file = open('./sharit/VERSION','r')
program_version = version_file.readline()
version_file.close()

user_agent="{program}/{version}".format(program=program_name, version=program_version, end='')

def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m sharit` and `$ sharit `.
    """



    print("Welcome to {program} {version}".format(program=program_name, version=program_version, end=''))

    parser = argparse.ArgumentParser(
      prog=program_name,
      description=program_description,
      epilog="Thanks for using %(prog)s! :)",
    )

    parser.add_argument("-u", "--url", required=True, help="The URL to share")
    parser.add_argument("-rcid", "--reddit-client-id", required=True, help="The Reddit Client ID")
    parser.add_argument("-rs", "--reddit-secret", required=True, help="The Reddit secret")
    parser.add_argument("-ru", "--reddit-username", required=True, help="The Reddit username")
    parser.add_argument("-rp", "--reddit-password", required=True, help="The Reddit password")
    parser.add_argument("-tak", "--twitter-api-key", required=True, help="The Twitter API key")
    parser.add_argument("-task", "--twitter-api-secret-key", required=True, help="The Twitter API secret key")
    parser.add_argument("-swu", "--slack-webhook-url", required=True, help="The Slack Webhook URL")
    parser.add_argument("-sr", "--sub-reddit", required=True, help="The sub-reddit to share the URL to")

    args = parser.parse_args()

    if not validators.url(args.url):
      sys.exit('Invalid URL')

    if not args.reddit_client_id:
      sys.exit("Invalid Reddit Client ID")

    if not args.reddit_secret:
      sys.exit("Invalid Reddit secret")

    if not args.reddit_username:
      sys.exit("Invalid Reddit username")

    if not args.reddit_password:
              sys.exit("Invalid Reddit password")

    if not args.twitter_api_key:
      sys.exit("Invalid Twitter API key")

    if not args.twitter_api_secret_key:
      sys.exit("Invalid Twitter API secret key")

    if not validators.url(args.slack_webhook_url):
      sys.exit("Invalid Slack Webhook URL")

    if not args.sub_reddit:
      sys.exit("Invalid Sub-Reddit")

    url_to_share=args.url

    # Set up credentials for different APIs
    REDDIT_CLIENT_ID = args.reddit_client_id
    REDDIT_SECRET = args.reddit_secret
    REDDIT_USERNAME = args.reddit_username
    REDDIT_PASSWORD = args.reddit_password
    TWITTER_API_KEY = args.twitter_api_key
    TWITTER_API_SECRET_KEY = args.twitter_api_secret_key
    SLACK_WEBHOOK_URL = args.slack_webhook_url
    SUB_REDDIT_NAME = args.sub_reddit

    post_to_reddit(SUB_REDDIT_NAME, url_to_share, REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD)

# Function to publish the URL on Reddit
def post_to_reddit(sub_reddit, url, reddit_client_id, reddit_secret, reddit_username, reddit_password):
  print("Sharing [{url}] on sub-reddit [{sub_reddit}]".format(url=url,sub_reddit=sub_reddit, end=''))

  reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_secret,
    username=reddit_username,
    password=reddit_password,
    user_agent="{program_name} by u/lechtitseb".format(program_name=program_name, end='')
  )

  subreddit = reddit.subreddit(sub_reddit)
  page = urllib.urlopen(url)
  page_contents = lxml.html.parse(page)
  title = page_contents.find(".//title").text

  try:
    submission_id = subreddit.submit(title, url=url)
  except praw.exceptions.RedditAPIException as e:
    print(f'Error posting to Reddit: {e}')
