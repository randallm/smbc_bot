#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import requests
import json
import feedparser
import urlparse

headers = {'user-agent': 'SMBC comic poster bot by /u/randallrocks'}

with open('auth.txt', 'r') as f:
    auth_info = f.readlines()
    auth = {'user': auth_info[0].rstrip(),
            'passwd': auth_info[1],
            'api_type': 'json'}

client = requests.session(headers=headers)
login_req = client.post('https://ssl.reddit.com/api/login', data=auth)

response = json.loads(login_req.text)
client.modhash = response['json']['data']['modhash']

smbc_feed = feedparser.parse('http://feeds.feedburner.com/smbc-comics/PvLb?format=xml')
latest_comic = smbc_feed.entries[0]

with open('latest.txt', 'r+') as f:
    if latest_comic.published != f.readlines()[0].rstrip():
        url = latest_comic.feedburner_origlink

        title = urlparse.urlparse(url).query
        title = urlparse.parse_qs(title)['id'][0]
        title += ': %s' % (latest_comic.title)
        title = '#' + title

        submission_info = {'uh': client.modhash,
                           'kind': 'link',
                           'url': url,
                           'sr': 'SMBC_comics',
                           'title': title}
        comic_post_req = client.post('https://ssl.reddit.com/api/submit',
                                     data=submission_info)

        f.seek(0)
        f.write(latest_comic.published)
    else:
        exit(0)
