#!/usr/bin/env python3
import requests
import uuid
import sys
import re
import builtins

def downloadImageFromUrl(url, path):
    if not url.startswith('http'):
        return None
    img_data = requests.get(url).content
    fPath = path+'/'+str(uuid.uuid1())+'.jpg'
    with open(fPath, 'wb') as handler:
        handler.write(img_data)
    return fPath

def print(ftext, **args):
    if sys.stdout.isatty():
        builtins.print (ftext, flush=True, **args)
    else:
        builtins.print(re.sub('\33\[\d+m',' ',ftext), flush=True, **args)
