#!/usr/bin/env python3
import os
import utils

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

title = '江苏大学欢迎您！'
desc = '江苏大学官方主页 - 工科特色鲜明、多学科协调发展的高水平研究型大学'

redirect = os.getenv('REDIRECT')

if redirect is None:
    redirect = 'https://www.ujs.edu.cn/'
    utils.print(f'{G}[+] {C}Redirect URL : {W}{redirect} (default)')
else:
    utils.print(f'{G}[+] {C}Redirect URL : {W}{redirect}')

with open('template/university/index_temp.html', 'r') as temp_index:
    temp_index_data = temp_index.read()
    temp_index_data = temp_index_data.replace('$TITLE$', title)
    temp_index_data = temp_index_data.replace('$DESC$', desc)
    temp_index_data = temp_index_data.replace('REDIRECT_URL', redirect)
    if os.getenv("DEBUG_HTTP"):
        temp_index_data = temp_index_data.replace('window.location = "https:" + restOfUrl;', '')

with open('template/university/index.html', 'w') as updated_index:
    updated_index.write(temp_index_data)
