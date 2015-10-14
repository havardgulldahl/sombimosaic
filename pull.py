#encoding:utf-8
#

import requests, logging, json, os.path

logging.basicConfig(level=logging.INFO)

SOMBIURL='http://sombi.nrk.no/api/1.2/data/?limit={limit}&skip={skip}&moderation=1&metadataQuery=true&project_id=552e77b7fd3cf1c636eda6d7'
LIMITREQUESTS=500

def sombiiter(session):
  c = 1
  start = session.get(SOMBIURL.format(limit=1, skip=0)) # get first record
  totalrecords = start.json()['metadata']['count']
  logging.info('Total %s records', totalrecords)
  while c < totalrecords:
    logging.info('Gettting %s SOMBIes, skipping %s', LIMITREQUESTS, c)
    r = session.get(SOMBIURL.format(limit=LIMITREQUESTS, skip=c))
    for record in r.json()['results']:
      yield record
    c = c + LIMITREQUESTS

if __name__ == '__main__':
  folder = './sombies'
  sess = requests.Session()
  for sombi in sombiiter(session=sess):
    logging.debug('Got new sombie: %s', sombi['id'])
    sidecar = os.path.join(folder, sombi['id'] + '.json')
    pngfile = os.path.join(folder, sombi['id'] + '.png')
    with open(sidecar, 'wb') as sf:
      sf.write(json.dumps(sombi))
      logging.debug('Wrote JSON: %s', sombi['title'])
    if not os.path.exists(pngfile):
      with open(pngfile, 'wb') as pf:
        pf.write(sess.get(sombi['image']['standard']).content)
        logging.debug('Wrote PNG: %s', sombi['title'])



