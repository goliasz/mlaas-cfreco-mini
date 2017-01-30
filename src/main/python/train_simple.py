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

def train():
  print "Training"  
  with open(args.input) as f:
    lines = f.readlines()

  for i in lines:
    #print i
    event = json.loads(i)
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
  parser.add_argument('--input', default="data/sample_training.json")
  parser.add_argument('--recourl', default="http://localhost:5000/api/v1.0/router")

  args = parser.parse_args()
  print "input",args.input
  print "recourl",args.recourl

  train()
  
