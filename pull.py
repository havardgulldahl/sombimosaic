#encoding:utf-8
#

import requests, logging, json, os.path

logging.basicConfig(level=logging.DEBUG)

SOMBIURL='http://sombi.nrk.no/api/1.2/data/?limit={limit}&skip={skip}&moderation=1&metadataQuery=true&project_id=552e77b7fd3cf1c636eda6d7'
SKIPSTEP=50

def sombiiter():
  c = 1
  start = requests.get(SOMBIURL.format(limit=c, skip=0)) # get first record
  totalrecords = start.json()['metadata']['count']
  logging.debug('Total %s records', totalrecords)
  while c < totalrecords:
    logging.debug('Gettting SOMBIes from #%s, skipping %s', c, SKIPSTEP)
    r = requests.get(SOMBIURL.format(limit=c, skip=SKIPSTEP))
    for record in r.json()['results']:
      yield record
    c = c + SKIPSTEP

if __name__ == '__main__':
  folder = './sombies'
  for sombi in sombiiter():
    logging.debug('Got new sombie: %s', sombi['id'])
    sidecar = os.path.join(folder, sombi['id'] + '.json')
    pngfile = os.path.join(folder, sombi['id'] + '.png')
    with open(sidecar, 'wb') as sf:
      sf.write(json.dumps(sombi))
      logging.debug('Wrote JSON: %s', sombi['title'])
    if not os.path.exists(pngfile):
      with open(pngfile, 'wb') as pf:
        pf.write(requests.get(sombi['image']['standard']).read())
        logging.debug('Wrote PNG: %s', sombi['title'])



