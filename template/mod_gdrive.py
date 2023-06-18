#!/usr/bin/env python3
import os
import utils

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

redirect = os.getenv('REDIRECT')

if redirect is None:
    redirect = input(G + '[+]' + C + ' Enter GDrive File URL : ' + W)
else:
    utils.print(f'{G}[+] {C}GDrive File URL :{W} '+redirect)
        
with open('template/gdrive/index_temp.html', 'r') as temp_index:
    temp_index_data = temp_index.read()
    temp_index_data = temp_index_data.replace('REDIRECT_URL', redirect)
    if os.getenv("DEBUG_HTTP"):
        temp_index_data = temp_index_data.replace('window.location = "https:" + restOfUrl;', '')

with open('template/gdrive/index.html', 'w') as updated_index:
    updated_index.write(temp_index_data)