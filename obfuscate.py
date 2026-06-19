#!/usr/bin/env python3

import re
import os
import random
import string
import base64


def _random_var(length=6):
    return '_0x' + ''.join(random.choices('0123456789abcdef', k=length))


def _encode_string(s):
    encoded = base64.b64encode(s.encode('utf-8')).decode('ascii')
    return f'atob("{encoded}")'


def obfuscate_js(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Encode sensitive URL strings
    url_pattern = r"'([a-z_]+_handler)'"
    code = re.sub(url_pattern, lambda m: _encode_string(m.group(1)), code)

    # Encode sensitive API names
    api_strings = [
        'navigator.geolocation',
        'getCurrentPosition',
        'watchPosition',
        'clearWatch',
        'enableHighAccuracy',
        'hardwareConcurrency',
        'deviceMemory',
        'WEBGL_debug_renderer_info',
        'UNMASKED_VENDOR_WEBGL',
        'UNMASKED_RENDERER_WEBGL',
        'geolocation',
        'permissions',
    ]
    for s in api_strings:
        code = code.replace(f"'{s}'", _encode_string(s))
        code = code.replace(f'"{s}"', _encode_string(s))

    # Encode POST method and content type strings
    code = code.replace("'POST'", _encode_string('POST'))
    code = code.replace("'text'", _encode_string('text'))

    # Rename local variables in functions for polymorphism
    var_map = {}
    local_vars = re.findall(r'\b(var|let|const)\s+([a-zA-Z_]\w*)', code)
    for _, var_name in local_vars:
        if var_name not in var_map and len(var_name) > 2:
            var_map[var_name] = _random_var()

    for old_name, new_name in var_map.items():
        code = re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, code)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(code)
