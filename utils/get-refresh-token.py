#!/usr/bin/env python

import argparse
import praw
import random
import socket
import sys

program_name="GetRedditRefreshToken"
program_description="Get a Reddit refresh token"

user_agent="{program}/{version}".format(program=program_name, version="0.0.1", end='')

def main():
  parser = argparse.ArgumentParser(
      prog=program_name,
      description=program_description,
      epilog="Thanks for using %(prog)s! :)",
    )

  parser.add_argument("-rcid", "--reddit-client-id", required=True, help="The Reddit Client ID")
  parser.add_argument("-rs", "--reddit-secret", required=True, help="The Reddit secret")

  args = parser.parse_args()

  if not args.reddit_client_id:
    sys.exit("Invalid Reddit Client ID")

  if not args.reddit_secret:
    sys.exit("Invalid Reddit secret")

  # Credentials
  REDDIT_CLIENT_ID = args.reddit_client_id
  REDDIT_SECRET = args.reddit_secret

  # API scopes to request
  scopes = ["submit"]

  reddit = praw.Reddit(
    redirect_uri="http://localhost:8080",
    user_agent="obtain_refresh_token/v0 by u/bboe",
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET
  )
  state = str(random.randint(0, 65000))
  url = reddit.auth.url(duration="permanent", scopes=scopes, state=state)
  print(f"Now open this url in your browser: {url}")

  client = receive_connection()
  data = client.recv(1024).decode("utf-8")
  param_tokens = data.split(" ", 2)[1].split("?", 1)[1].split("&")
  params = {
    key: value for (key, value) in [token.split("=") for token in param_tokens]
  }

  if state != params["state"]:
    send_message(
        client,
        f"State mismatch. Expected: {state} Received: {params['state']}",
    )
    return 1
  elif "error" in params:
    send_message(client, params["error"])
    return 1

  refresh_token = reddit.auth.authorize(params["code"])
  send_message(client, f"Refresh token: {refresh_token}")
  return 0


def receive_connection():
    """Wait for and then return a connected socket..

    Opens a TCP connection on port 8080, and waits for a single client.

    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client


def send_message(client, message):
    """Send message to client and close the connection."""
    print(message)
    client.send(f"HTTP/1.1 200 OK\r\n\r\n{message}".encode("utf-8"))
    client.close()


if __name__ == "__main__":
    sys.exit(main())
