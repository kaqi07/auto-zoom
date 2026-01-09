# zoom 自动化（简易版）

## 功能
- 通过 Zoom REST API 自动创建会议，并在本机自动打开加入/开始链接
- 将本地视频文件推流到“虚拟摄像头”，在 Zoom 里当作摄像头使用（无需真实摄像头）

## 准备
1. Zoom 后台创建 **Server-to-Server OAuth** 应用，拿到 `account_id / client_id / client_secret`
2. 确保有一个可创建会议的 Zoom 用户（邮箱或 userId）
3. 安装 Zoom 桌面客户端
4. 需要“虚拟摄像头”驱动（推荐安装 OBS 并启用 Virtual Camera）

## 配置
```bash
cp .env.example .env
```
在 `.env` 填入：
- `ZOOM_ACCOUNT_ID`
- `ZOOM_CLIENT_ID`
- `ZOOM_CLIENT_SECRET`
- `ZOOM_USER_ID`

## 运行
安装依赖（本项目用 uv）：
```bash
uv sync
```
如果下载超时：
```bash
UV_HTTP_TIMEOUT=300 uv sync
```

创建并打开会议（默认打开 host 的 start_url）：
```bash
uv run -m zoom_automation.meeting --topic "demo" --name "bot" --open start
```

把视频文件当作摄像头输出（先在 Zoom 里把摄像头切到对应的虚拟摄像头设备）：
```bash
uv run -m zoom_automation.virtual_camera --video /path/to/video.mp4 --loop
```
macOS：首次启用虚拟摄像头可能需要在系统设置里允许 OBS 的系统扩展并重启。
