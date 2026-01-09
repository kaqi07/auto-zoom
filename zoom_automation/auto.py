"""Create a Zoom meeting, open it, and stream a video as a virtual camera."""

import argparse
import os
import threading
import time
import webbrowser

from dotenv import load_dotenv

from zoom_automation.meeting import create_instant_meeting, get_access_token, zoommtg_join_url
from zoom_automation.virtual_camera import play_video


def main() -> None:
    """Create a meeting, open Zoom, and stream a local video as the camera.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    load_dotenv()
    p = argparse.ArgumentParser()
    p.add_argument("--video", required=True)
    p.add_argument("--device", default=None)
    p.add_argument("--loop", action="store_true")
    p.add_argument("--topic", default="auto meeting")
    p.add_argument("--name", default="bot")
    p.add_argument("--open", choices=["start", "join", "none"], default="start")
    p.add_argument("--delay", type=float, default=0.5)
    a = p.parse_args()

    token = get_access_token(os.environ["ZOOM_ACCOUNT_ID"], os.environ["ZOOM_CLIENT_ID"], os.environ["ZOOM_CLIENT_SECRET"])
    m = create_instant_meeting(token, os.environ["ZOOM_USER_ID"], a.topic)
    print("id:", m["id"])
    print("join_url:", m["join_url"])
    print("start_url:", m["start_url"])

    t = threading.Thread(target=play_video, args=(a.video, a.device, a.loop))
    t.start()
    time.sleep(a.delay)
    if a.open == "start":
        webbrowser.open(m["start_url"])
    if a.open == "join":
        webbrowser.open(zoommtg_join_url(m["join_url"], a.name))
    t.join()


if __name__ == "__main__":
    main()

