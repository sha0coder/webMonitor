#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @sha0coder

import sys
import requests
import time
import csv

uagent = {
    'android': 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'firefox': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
}

print('Welcome to web reliability monitor, coded by jolmos')

# INPUT SETTING
ua = raw_input('Select User-Agent, [A]ndroid or [F]irefox? [A/F] ').upper()
if ua == 'F':
    user_agent = uagent['firefox']
elif ua == 'A':
    user_agent = uagent['android']
else:
    print('select a correct user agent.')
    sys.exit()

url = raw_input('Select target Url: ')
delay = int(raw_input('Select monitoring delay in seconds: '))
outfile = raw_input('Output filename: ')
fd = open(outfile, 'wt')
writer = csv.writer(fd)
writer.writerow(('time', 'code', 'size', 'millis', 'err', 'url'))

def check(url, user_agent):
    init = time.time()
    err = 'ok'
    code = 0
    sz = 0
    try:
        resp = requests.get(url, verify=False, allow_redirects=False, timeout=(delay+4), headers={
            'User-Agent': user_agent
        })
        code = resp.status_code
        sz = len(resp.text)

    except requests.exceptions.ConnectionError:
        err = 'cant connect'
    except requests.exceptions.MissingSchema:
        err = 'bad url'
    except requests.exceptions.Timeout:
        err = 'timeout'
    '''
    except Exception as msg:
        err = msg
    except:
        err = 'fail'
    '''


    secs = int(round(time.time() - init, 4)*1000)
    return err, code, sz, secs


raw_input('Press enter to start.')
print('Monitoring ...')
avg = 0
all_millis = []

try:
    while True:
        t = time.ctime()
        err, code, sz, millis = check(url, user_agent)
        all_millis.append(millis)
        avg = reduce(lambda x, y: x + y, all_millis) / len(all_millis)

        print('[%s] code:%d sz:%d millis:%d avg:%d err:%s => %s' % (t, code, sz, millis, avg, err, url))
        writer.writerow((t, code, sz, millis, err, url))
        time.sleep(delay)


except KeyboardInterrupt:
    fd.close()
    sys.exit()


