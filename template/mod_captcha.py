#!/usr/bin/env python3

import os
import shutil

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

forward = input(G + '[+]' + C + ' Forward to : ' + W)

with open('template/captcha/js/location_temp.js', 'r') as location_temp:
    loc = location_temp.read()
    loc = loc.replace('$FORWARDEDWEBSITE$', forward)
with open('template/captcha/js/location.js','w') as new_loc:
    #print(loc)
    new_loc.write(loc)