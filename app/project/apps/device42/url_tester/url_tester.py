"""
url_tester.py
written by:   dave.amato@device42.com
description:  CLI python script
"""
import requests, os
GOOD_URLS = []
BAD_URLS = []
dir_path = os.path.dirname(os.path.realpath(__file__))

def write_results():
  with open(os.path.join(dir_path, 'url_tester.log'), 'a') as g:
    g.write('\n----------------------')
    g.write('\nGOOD URLs (%s)\n' % len(GOOD_URLS))
    for gu in GOOD_URLS:
      g.write(gu)
    g.write('\nBAD URLs (%s)\n' % len(BAD_URLS))
    for bu in BAD_URLS:
      g.write(bu)
    g.write('\nComplete!')
    g.close()

with open(os.path.join(dir_path, 'urls.txt'), 'r') as f:
  lines = f.readlines()
  for l in lines:
    if 'http' in l:
      print('getting %s' % l)
      r = requests.get(l)
      if r.status_code == 200:
        GOOD_URLS.append(l)
      else:
        BAD_URLS.append(l)
  f.close()
  print('Complete!')
write_results()
