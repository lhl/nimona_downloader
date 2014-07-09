#!/usr/bin/env python


import glob
import logging
from   lxml import html
import os
import requests
import shutil
import sys
import time
import urllib


# Logging
logging.basicConfig(level=logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s : %(levelname)-8s : %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


# Locations
HOME = os.path.dirname(os.path.realpath(__file__))
CWD  = os.getcwd()


# Make folder if it doesn't exist
ARCHIVE = '%s/nimona' % CWD
if not os.path.isdir(ARCHIVE):
  logging.info('Creating archive: %s' % ARCHIVE)
  os.makedirs(ARCHIVE)


# Find last node in our archive...
files = glob.glob('%s/*.jpg' % ARCHIVE)
if files:
  next_node = int(os.path.basename(files[-1]).split('-')[0]) + 1
else:
  next_node = 22 # This is the first page
logging.info('Next node: %s' % next_node)


# Get the last node on the site
r = requests.get('http://gingerhaze.com/nimona')
p = html.fromstring(r.text)
last_node = int(p.xpath('///div[contains(@class, "node")]/@id')[0].split('-')[1])
logging.info('Last node: %s' % last_node)



# UP AND ATOM
for i in range(next_node, last_node+1):
  logging.info('GET node: %s' % next_node)
  r = requests.get('http://gingerhaze.com/node/%s' % next_node)

  # Exit once we reach the end
  if not r.ok:
    logging.info('SKIP no node found...')
  
  # Get Image
  p = html.fromstring(r.text)
  m = p.xpath('//img[@typeof="foaf:Image"]/@src')

  # Skip to next page, doesn't have image...
  if not len(m):
    logging.info('SKIP No image found...')
  else:
    img = m[0]
    logging.info('IMG FOUND: %s' % img)

    # Download Image
    dl = '%s/%04d-%s' % (ARCHIVE, 
                         next_node, 
                         urllib.unquote(os.path.basename(img))
                        )
    logging.info('SAVING to %s' % dl) 

    r = requests.get(img, stream=True)
    with open(dl, 'wb') as f:
      shutil.copyfileobj(r.raw, f)

  # DEBUG
  # sys.exit()

  next_node += 1

  # Be nice
  time.sleep(1)
