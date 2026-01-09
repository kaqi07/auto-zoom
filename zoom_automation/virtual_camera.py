"""Stream a local video file into a virtual camera device for Zoom."""

import argparse

import cv2
import pyvirtualcam


def play_video(video_path: str, device: str | None, loop: bool) -> None:
    """Play a video file as a virtual camera stream.

    Parameters
    ----------
    video_path : str
        Path to a local video file (e.g. mp4), shape=().
    device : str | None
        Target virtual camera device name or ``None`` for default, shape=().
    loop : bool
        Whether to loop the video forever, shape=().

    Returns
    -------
    None
    """
    cap = cv2.VideoCapture(video_path)
    w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    with pyvirtualcam.Camera(w, h, fps, device=device, fmt=pyvirtualcam.PixelFormat.BGR) as cam:
        while True:
            ok, frame = cap.read()
            if not ok:
                if loop:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                break
            cam.send(frame)
            cam.sleep_until_next_frame()


def main() -> None:
    """Parse CLI args and start virtual camera streaming.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    p = argparse.ArgumentParser()
    p.add_argument("--video", required=True)
    p.add_argument("--device", default=None)
    p.add_argument("--loop", action="store_true")
    a = p.parse_args()
    play_video(a.video, a.device, a.loop)


if __name__ == "__main__":
    main()
