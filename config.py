#!/usr/bin/python

config = {}

config['plexify'] = {
    'plex_api': {
        'protocol': 'http',
        'host': '192.168.1.112:32400',
        'path': '/library/recentlyAdded'
    },
    'smtp': {
        'server': 'smtp.gmail.com',
        'port': 587,
        'username': '',
        'password': '',
        'from': 'plex@local',
        'to': ''
    }
}

def get_config():
    return config['plexify']
