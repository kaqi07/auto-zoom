# Zoom Meeting Automation (Minimal)

## What it does
- Create a Zoom meeting via REST API and open the start/join URL locally
- Stream a local video file to a virtual camera (no physical camera)

## Prerequisites
1. Zoom App Marketplace: create a **Server-to-Server OAuth** app and get `account_id / client_id / client_secret`
2. A Zoom user that can create meetings (`ZOOM_USER_ID` can be an email)
3. Zoom desktop client installed
4. A virtual camera driver (OBS Virtual Camera recommended)

## Setup
```bash
cp .env.example .env
```
Fill in `.env`:
- `ZOOM_ACCOUNT_ID`
- `ZOOM_CLIENT_ID`
- `ZOOM_CLIENT_SECRET`
- `ZOOM_USER_ID`

## Run
Install deps (uv):
```bash
uv sync
```

Create + open meeting:
```bash
uv run -m zoom_automation.meeting --topic "demo" --name "bot" --open start
```

Stream video to virtual camera:
```bash
uv run -m zoom_automation.virtual_camera --video <path_to_video> --loop
```

All-in-one: create meeting + open Zoom + stream video (Ctrl+C to stop streaming):
```bash
uv run -m zoom_automation.auto --topic "demo" --name "bot" --open start --video <path_to_video> --loop
```

Notes:
- In Zoom, select the virtual camera device as your camera.
- On macOS, OBS Virtual Camera may require allowing a system extension and rebooting.
