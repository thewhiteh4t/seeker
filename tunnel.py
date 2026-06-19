#!/usr/bin/env python3

import re
import subprocess
import threading
from time import sleep, time


def start_tunnel(provider, port):
    if provider == 'cloudflare':
        return _start_cloudflare(port)
    elif provider == 'ngrok':
        return _start_ngrok(port)
    elif provider == 'localhost.run':
        return _start_localhost_run(port)
    elif provider == 'serveo':
        return _start_serveo(port)
    else:
        raise ValueError(f'Unknown tunnel provider: {provider}')


def _start_cloudflare(port):
    cmd = ['cloudflared', 'tunnel', '--url', f'http://127.0.0.1:{port}', '--no-autoupdate']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    url = _wait_for_url(proc, r'https://[a-z0-9-]+\.trycloudflare\.com', timeout=30)
    return url, proc


def _start_ngrok(port):
    cmd = ['ngrok', 'http', str(port), '--log=stdout']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    url = _wait_for_url(proc, r'https://[a-z0-9-]+\.ngrok[a-z0-9.-]*\.com', timeout=20)
    return url, proc


def _start_localhost_run(port):
    cmd = ['ssh', '-o', 'StrictHostKeyChecking=no', '-R', f'80:localhost:{port}', 'localhost.run']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    url = _wait_for_url(proc, r'https://[a-z0-9-]+\.lhr\.life', timeout=20)
    return url, proc


def _start_serveo(port):
    cmd = ['ssh', '-o', 'StrictHostKeyChecking=no', '-R', f'80:localhost:{port}', 'serveo.net']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    url = _wait_for_url(proc, r'https://[a-z0-9-]+\.serveo\.net', timeout=20)
    return url, proc


def _wait_for_url(proc, pattern, timeout=30):
    url_holder = [None]
    lines = []

    def _reader():
        for line in iter(proc.stdout.readline, ''):
            lines.append(line)
            match = re.search(pattern, line)
            if match:
                url_holder[0] = match.group(0)
                return

    reader_thread = threading.Thread(target=_reader, daemon=True)
    reader_thread.start()
    reader_thread.join(timeout=timeout)

    return url_holder[0]
