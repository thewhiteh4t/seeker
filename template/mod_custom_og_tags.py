#!/usr/bin/env python3

import os
import utils

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

redirect = os.getenv('REDIRECT')
sitename = os.getenv('SITENAME')
title = os.getenv('TITLE')
imageUrl = os.getenv('IMAGE')
desc = os.getenv("DESC")

old = 'n'
if not redirect and not sitename and not title and not imageUrl and not desc:
    old = input(G + '[+]' + C + ' Do you want to reuse previous configs? (Y/N) : ' + W)

if old.lower() != 'y':
    if redirect is None:
        redirect = input(G + '[+]' + C + ' Enter Target URL (YouTube,Blog etc) : ' + W)
    else:
        utils.print(f'{G}[+] {C}Target URL :{W} '+redirect)
    
    if sitename is None:
        sitename = input(G + '[+]' + C + ' Site Name: ' + W)
    else:
        utils.print(f'{G}[+] {C}Site Name :{W} '+sitename)
    
    if title is None:
        title = input(G + '[+]' + C + ' Title : ' + W)
    else:
        utils.print(f'{G}[+] {C}Title :{W} '+title)
    
    if imageUrl is None:
        imageUrl = input(G + '[+]' + C + ' Image URL: ' + W)
    else:
        utils.print(f'{G}[+] {C}Image :{W} '+imageUrl)
    
    if desc is None:
        desc = input(G + '[+]' + C + ' Description: ' + W)
    else:
        utils.print(f'{G}[+] {C}Description :{W} '+desc)

    with open('template/custom_og_tags/index_temp.html', 'r') as index_temp:
        code = index_temp.read()
        if os.getenv("DEBUG_HTTP"):
            code = code.replace('window.location = "https:" + restOfUrl;', '')
        code = code.replace('$SITE_NAME$', sitename)
        code = code.replace('REDIRECT_URL', redirect)
        code = code.replace('$TITLE$', title)
        code = code.replace('$IMG_URL$', imageUrl)
        code = code.replace('$DESCRIPTION$', desc)

    with open('template/custom_og_tags/index.html', 'w') as new_index:
        new_index.write(code)
