#!/usr/bin/env python

# Copyright (C) KOLIBERO Piotr Goliasz - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Piotr Goliasz <piotr.goliasz@kolibero.eu>, December 2016

import json
import argparse
import requests

def query():
  print "Query"  
  qry = {"rtype":"query", "size":"10"}
  
  items = args.items.split(",")
  #print items
  if len(items) > 1:
    print items
    qry["items"] = items  
  else:
    qry["item_id"] = items[0]

  print qry

  resp = requests.post(args.recourl,data=json.dumps(qry),headers={'Content-Type':'application/json'})
  if resp:
    if resp.status_code != 200:
      raise Exception('POST failed {}'.format(resp.status_code))
    else:
      result = resp.json()
      print result

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Query Util")
  parser.add_argument('--recourl', default="http://localhost:5000/api/v1.0/router")
  parser.add_argument('--items')

  args = parser.parse_args()
  print "recourl",args.recourl
  print "items",args.items

  query()
  
