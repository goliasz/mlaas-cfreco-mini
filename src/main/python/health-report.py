#!/usr/bin/python

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

import argparse
import base64
import json
import sys
import time
import os
import requests
import memcache
from random import randint

def read_file(p_file):
  data = ''
  with open(p_file) as myfile:
    data="<BR>".join(line.rstrip() for line in myfile)
  return data

def report_health():
  #
  url = read_file('/tmp/H_TARGET').strip("<BR>")
  if not url:
    url = "http://kolibero.ddns.net:8081/api/v1.0/health/"
  
  #
  id = read_file('/tmp/H_ID')
  url += id 
  type = read_file('/tmp/H_TYPE')
  appl = read_file('/tmp/H_APPL')
  appl_id = read_file('/tmp/H_APPL_ID')
  id_short = read_file('/tmp/H_ID_SHORT')
  #touch = read_file('/tmp/H_TOUCH')
  ps = read_file('/tmp/H_PS')
  #
  reco_message = {}
  try:
    print("Connection to MemCached")
    mc = memcache.Client(['localhost:11211'], debug=0)

    latency_query = mc.get("latency_query")
    latency_train = mc.get("latency_train")
    message_query = mc.get("message_query")
    message_train = mc.get("message_train")
    response_query = mc.get("response_query")
    response_train = mc.get("response_train")
    query_cnt = mc.get("query_cnt")
    train_cnt = mc.get("train_cnt")
    qresp_empty = mc.get("qresp_empty")
    qresp_ok = mc.get("qresp_ok")
    reco_message = {"latency_query":latency_query,
                    "latency_train":latency_train,
                    "message_query":message_query,
                    "message_train":message_train,
                    "response_query":response_query,
                    "response_train":response_train,
                    "query_cnt":query_cnt,
                    "train_cnt":train_cnt,
                    "qresp_empty":qresp_empty,
                    "qresp_ok":qresp_ok}
  except Exception,Argument:
    reco_message["error"] = str(Argument)
  #
  msg = {"id":id,
         "millis":(time.time()*1000),
         "type":type,
         "appl":appl,
         "appl_id":appl_id,
         "id_short":id_short,
         #"touch":touch,
         "msg":reco_message,
         "ps":ps}
  msgstr = json.dumps(msg)

  #print url
  #print msgstr
  #
  resp = requests.post(url, data=msgstr, headers={'Content-Type':'application/json'})
  if resp.status_code != 200:
    raise Exception('POST failed {}'.format(resp.status_code))
  print resp.json()

if __name__ == '__main__':
  time.sleep(randint(0,9))
  report_health()

