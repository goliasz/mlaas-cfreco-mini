#!/usr/bin/env python

# Copyright KOLIBERO under one or more contributor license agreements.
# KOLIBERO licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import argparse
import hashlib
import requests

def prepare_training_data(src_fname):
  content = None
  with open(src_fname) as f:
    content = f.readlines()

  events0 = {}
  offset = 0
  last_timestamp = 0
  for i in content:
    jc = json.loads(i)   
    if jc:
      period_no = int(jc.get("timestamp"))/(int(args.period)*1000)
      userid = jc.get("userid")
      cart_no = str(period_no)+"_"+userid
      #print cart_no, jc.get("fullname")
      cart = events0.get(cart_no)
      if not cart:
        items = {jc.get("courseid"):1}
        #print jc        
        events0[cart_no] = {"user_id":userid,"user_name":jc.get("fullname"),"items":items}
      else:
        items = cart.get("items")
        count = items.get(jc.get("courseid"),0)
        items[jc.get("courseid")] = count + 1
        cart["items"] = items
        events0[cart_no] = cart
  #
  #print "---------------------------"
  #print events0
  #print "---------------------------"
  #
  event = {}
  events = []
  for i in events0.items():
    #print i[1]
    e = i[1]
    #print type(e)
    #print e["user_id"]
    event["user_id"] = e.get("user_id")
    items = []
    for i in e["items"].items():
      items.append(i[0])
    event["items"] = items
    #print items
    #print event
    events.append(event)
  #
  return events

def train(p_data):
  print "Training"  
  for i in p_data:
    #print i
    event = i
    event["rtype"] = "train"
    print event
    resp = requests.post(args.recourl,data=json.dumps(event),headers={'Content-Type':'application/json'})
    if resp:
      if resp.status_code != 200:
        raise Exception('POST failed {}'.format(resp.status_code))
      else:
        result = resp.json()
        print result

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Training file preprocessor")
  parser.add_argument('--src', default="data/courseInfo_with_cookie.json")
  parser.add_argument('--period', default="604800")
  parser.add_argument('--recourl', default="http://localhost:5000/api/v1.0/router")

  args = parser.parse_args()
  print "src",args.src
  print "period",args.period,"seconds"
  print "url",args.recourl

  data = prepare_training_data(args.src)
  train(data)
  
