import argparse
import json
import os
import praw
import requests
import sys
import validators
import lxml.html
import urllib.request as urllib
import slack_sdk as slack
from slack_sdk.errors import SlackApiError
import tweepy
from bs4 import BeautifulSoup

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
    parser.add_argument("-rrt","--reddit-refresh-token", required=True, help="The Reddit refresh token")
    parser.add_argument("-tak", "--twitter-api-key", required=True, help="The Twitter API key")
    parser.add_argument("-task", "--twitter-api-secret-key", required=True, help="The Twitter API secret key")
    parser.add_argument("-tat", "--twitter-access-token", required=True, help="The Twitter Access token")
    parser.add_argument("-tats", "--twitter-access-token-secret", required=True, help="The Twitter Access token secret")
    parser.add_argument("-sbt", "--slack-bot-token", required=True, help="The Slack Bot token")
    parser.add_argument("-sc", "--slack-channel", required=True, help="The Slack channel to share the URL to")
    parser.add_argument("-sr", "--sub-reddit", required=True, help="The sub-reddit to share the URL to")

    args = parser.parse_args()

    if not validators.url(args.url):
      print("URL: ", args.url)
      sys.exit('Invalid URL')

    if not args.reddit_client_id:
      sys.exit("Invalid Reddit Client ID")

    if not args.reddit_secret:
      sys.exit("Invalid Reddit secret")

    if not args.reddit_refresh_token:
      sys.exit("Invalid Reddit refresh token")

    if not args.twitter_api_key:
      sys.exit("Invalid Twitter API key")

    if not args.twitter_access_token:
      sys.exit("Invalid Twitter Access token")

    if not args.twitter_access_token_secret:
      sys.exit("Invalid Twitter API Access token secret")

    if not args.twitter_api_secret_key:
      sys.exit("Invalid Twitter API secret key")

    if not args.slack_bot_token:
      sys.exit("Invalid Slack Bot token")

    if not args.slack_channel:
      sys.exit("Invalid Slack channel")

    if not args.sub_reddit:
      sys.exit("Invalid Sub-Reddit")

    url_to_share=args.url

    # Set up credentials for different APIs
    REDDIT_CLIENT_ID = args.reddit_client_id
    REDDIT_SECRET = args.reddit_secret
    REDDIT_REFRESH_TOKEN = args.reddit_refresh_token
    TWITTER_API_KEY = args.twitter_api_key
    TWITTER_API_SECRET_KEY = args.twitter_api_secret_key
    TWITTER_ACCESS_TOKEN = args.twitter_access_token
    TWITTER_ACCESS_TOKEN_SECRET = args.twitter_access_token_secret
    SLACK_BOT_TOKEN = args.slack_bot_token
    SLACK_CHANNEL = args.slack_channel
    SUB_REDDIT_NAME = args.sub_reddit

    response = requests.get(url_to_share)
    soup = BeautifulSoup(response.content, 'html.parser')
    page_title = soup.title.string.strip()

    post_to_reddit(SUB_REDDIT_NAME, url_to_share, page_title, REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_REFRESH_TOKEN)
    post_to_slack(SLACK_CHANNEL, url_to_share, SLACK_BOT_TOKEN)
    post_to_twitter(url_to_share, TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

# Function to publish the URL on Reddit
def post_to_reddit(sub_reddit, url, title, reddit_client_id, reddit_secret, reddit_refresh_token):
  print("Sharing [{url}] on sub-reddit [{sub_reddit}]".format(url=url,sub_reddit=sub_reddit, end=''))

  reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_secret,
    refresh_token=reddit_refresh_token,
    user_agent="{program_name} by u/lechtitseb".format(program_name=program_name, end='')
  )

  subreddit = reddit.subreddit(sub_reddit)

  try:
    submission_id = subreddit.submit(title, url=url)
    print("Shared on Reddit")
  except praw.exceptions.RedditAPIException as e:
    print("Error posting on Reddit: {}".format(e))

# Function to publish the URL on Slack
def post_to_slack(channel, url, slack_bot_token):
  print("Sharing [{url}] on slack channel [{channel}]".format(url=url,channel=channel, end=''))

  slack_client = slack.WebClient(token=slack_bot_token)

  try:
    response = slack_client.chat_postMessage(
        channel=channel,
        text=url
    )
    print("Shared on Slack")
  except SlackApiError as e:
    print("Error posting on Slack: {}".format(e))

def post_to_twitter(url, api_key, api_key_secret, access_token, access_token_secret):
  print("Sharing [{url}] on Twitter".format(url=url))

  # Set up the API client
  api = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_key_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
  )

  try:
    api.create_tweet(text=url)
    print("Shared on Twitter")
  except tweepy.TweepyException as e:
    print("Error posting on Twitter: {}".format(e))
