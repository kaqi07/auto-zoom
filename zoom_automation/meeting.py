"""Create a Zoom meeting via REST API and open it locally."""

import argparse
import os
import webbrowser
from urllib.parse import parse_qs, urlencode, urlparse

import requests
from dotenv import load_dotenv


def get_access_token(account_id: str, client_id: str, client_secret: str) -> str:
    """Get a Zoom Server-to-Server OAuth access token.

    Parameters
    ----------
    account_id : str
        Zoom account ID, shape=().
    client_id : str
        Zoom OAuth client ID, shape=().
    client_secret : str
        Zoom OAuth client secret, shape=().

    Returns
    -------
    access_token : str
        Bearer token for Zoom REST API, shape=().
    """
    r = requests.post(
        "https://zoom.us/oauth/token",
        params={"grant_type": "account_credentials", "account_id": account_id},
        auth=(client_id, client_secret),
    )
    return r.json()["access_token"]


def create_instant_meeting(access_token: str, user_id: str, topic: str) -> dict:
    """Create an instant Zoom meeting for a given user.

    Parameters
    ----------
    access_token : str
        Zoom REST API bearer token, shape=().
    user_id : str
        Zoom user identifier (email or userId), shape=().
    topic : str
        Meeting topic, shape=().

    Returns
    -------
    meeting : dict
        Zoom meeting object (contains at least ``id``, ``join_url``, ``start_url``).
    """
    r = requests.post(
        f"https://api.zoom.us/v2/users/{user_id}/meetings",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"topic": topic, "type": 1},
    )
    return r.json()


def zoommtg_join_url(join_url: str, display_name: str) -> str:
    """Convert a web join URL into a zoommtg:// deep link.

    Parameters
    ----------
    join_url : str
        Zoom web join URL (e.g. ``https://zoom.us/j/<id>?pwd=...``), shape=().
    display_name : str
        Participant display name, shape=().

    Returns
    -------
    deeplink : str
        Zoom deep link URL (``zoommtg://``), shape=().
    """
    u = urlparse(join_url)
    meeting_id = u.path.rsplit("/", 1)[-1]
    pwd = parse_qs(u.query).get("pwd", [""])[0]
    return "zoommtg://zoom.us/join?" + urlencode({"confno": meeting_id, "pwd": pwd, "uname": display_name})


def main() -> None:
    """Create a meeting, print URLs, and open Zoom locally.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    load_dotenv()
    p = argparse.ArgumentParser()
    p.add_argument("--topic", default="auto meeting")
    p.add_argument("--name", default="bot")
    p.add_argument("--open", choices=["start", "join", "none"], default="start")
    a = p.parse_args()

    token = get_access_token(os.environ["ZOOM_ACCOUNT_ID"], os.environ["ZOOM_CLIENT_ID"], os.environ["ZOOM_CLIENT_SECRET"])
    m = create_instant_meeting(token, os.environ["ZOOM_USER_ID"], a.topic)
    print("id:", m["id"])
    print("join_url:", m["join_url"])
    print("start_url:", m["start_url"])
    if a.open == "start":
        webbrowser.open(m["start_url"])
    if a.open == "join":
        webbrowser.open(zoommtg_join_url(m["join_url"], a.name))


if __name__ == "__main__":
    main()

