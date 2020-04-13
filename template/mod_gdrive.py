#!/usr/bin/env python3

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

redirect = input(G + '[+]' + C + ' Enter GDrive File URL : ' + W)
with open('template/gdrive/js/location_temp.js', 'r') as js:
	reader = js.read()
	update = reader.replace('REDIRECT_URL', redirect)

with open('template/gdrive/js/location.js', 'w') as js_update:
	js_update.write(update)