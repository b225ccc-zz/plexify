#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
import sys
import logging
import time
from datetime import datetime
import config

config = config.get_config()

# set up logger
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname) -8s %(asctime)s m:%(module)s f:%(funcName)s l:%(lineno)d: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def notify_email(config, media_info):
    import smtplib
    from email.mime.text import MIMEText
    msg = MIMEText(media_to_list(media_info))
    msg['From'] = config['from']
    msg['To'] = config['to']
    msg['Subject'] = "New content in Plex - %s" % timestamp_pp()

    s = smtplib.SMTP(config['server'], config['port'])
    try:
        #s.set_debuglevel(True)
        s.ehlo()

        if s.has_extn('STARTTLS'):
            s.starttls()
            s.ehlo()

        s.login(config['username'], config['password'])
        s.sendmail(config['from'], [config['to']], msg.as_string())

    except:
        logger.error("problem connecting to mail server")
    finally:
        s.quit()
        
    return

def media_to_list(media):
    music = ['New music:']
    movies = ['\n\nNew movies:']
    tv = ['\n\nNew TV shows:']
    for m in media:
        if m['type'] == 'Music':
            music.append(' * %s - %s' % (m['artist'], m['album']))
        if m['type'] == 'Video':
            movies.append(' * %s' % m['title'])
        if m['type'] == 'TV Shows':
            tv.append(' * %s (%s)' % (m['show'], m['season']))

    r = ''
    if len(music) > 1:
        r = r + ('\n').join(music)
    if len(movies) > 1:
        r = r + ('\n').join(movies)
    if len(tv) > 1:
        r = r + ('\n').join(tv)

    return r

def timestamp_pp(stamp=time.time()):
    return datetime.fromtimestamp(float(stamp)).strftime('%Y-%m-%d %H:%M:%S')

try:
    f = open('cache.txt', 'r')
except:
    logger.info("No existing cache.txt found")
    last_timestamp = int(time.time())
else:
    last_timestamp = int(f.readline())
    f.close

try:
    f = open('pass.txt', 'r')
except:
    logger.info("No pass.txt found, using ''")
    config['smtp']['password'] = ''
else:
    password = f.readline().strip('\n')
    config['smtp']['password'] = password
    f.close

logger.info("Last run: %s" % timestamp_pp(last_timestamp))

url = "%s://%s%s" % (config['plex_api']['protocol'], config['plex_api']['host'], config['plex_api']['path'])
r = requests.get(url)
logger.debug("PLEX API return code: %i" % r.status_code)
soup = BeautifulSoup(r.text)

timestamp = int(time.time())
logger.debug("Current timestamp  = %i" % (timestamp))

media = []

def is_new(last_run_timestamp, media_timestamp):
    logger.debug('last_run_timestamp = %s, media_timestamp = %s' %(timestamp_pp(last_run_timestamp), timestamp_pp(media_timestamp)))
    if media_timestamp > last_run_timestamp:
        return True
    else:
        return False

a = soup.find_all('directory')
for e in a:
    media_type = e['librarysectiontitle']
    if is_new(last_timestamp, int(e['addedat'])):
        logger.debug("%s, %s, %s" % (e['librarysectiontitle'], e['parenttitle'], e['title']))
        if media_type == 'Music':
            media.append({
                'type': media_type,
                'artist': e['parenttitle'],
                'album': e['title'],
                'addedat': e['addedat']
                })
        elif media_type == 'TV Shows':
            media.append({
                'type': media_type,
                'show': e['parenttitle'],
                'season': e['title'],
                'addedat': e['addedat']
                })

a = soup.find_all('video')
for e in a:
    if is_new(last_timestamp, int(e['addedat'])):
        media.append({
            'type': 'Video',
            'title': e['title'],
            'addedat': e['addedat']
            })
        t = datetime.fromtimestamp(int(e['addedat'])).strftime('%Y-%m-%d %H:%M:%S')
        logger.debug("%s, %s, %s" % ('Video', e['title'], t))

if media:
    notify_email(config['smtp'], media)
    logger.debug(media)

f = open('cache.txt', 'w')
f.write("%s\n" % timestamp)
f.close()

logger.info('Run complete; %i new item(s)' % len(media))

sys.exit()
