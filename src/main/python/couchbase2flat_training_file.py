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

import json
import csv
import argparse
import hashlib
from couchbase.bucket import Bucket

def create_flat_array():
  couch = Bucket(args.couchbase)
  arr = []
  for row in couch.n1ql_query(args.n1ql):
    jrow = {"userid":row.get("userid"),"itemid":row.get("itemid"),"timebucket":row.get("timebucket")}
    arr.append(jrow)
  return arr

def create_grouped_array(p_flat_arr):
  grouped = {}
  for row in p_flat_arr:
    userid = str(row.get("userid"))
    timebucket = str(row.get("timebucket"))
    itemid = str(row.get("itemid").encode("utf-8"))
    group = grouped.get(userid+timebucket)
    if not group:
      group = {"user_id":userid,"items":[itemid]}
    else:
      items = group.get("items")
      items.append(itemid)
      items = {x:1 for x in items}.keys()       
      group["items"] = items
    grouped[userid+timebucket] = group
  return grouped 

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Couchbase 2 Flat Training")
  parser.add_argument('--couchbase', default="couchbase://localhost/bucketname")
  parser.add_argument('--n1ql', default="select bn.userid userid, bn.itemid itemid bn.day timebucket from bucketname bn")
  parser.add_argument('--output', default="data/training_data.json")
  
  args = parser.parse_args()
  print "couchbase:",args.couchbase
  print "n1ql:",args.n1ql
  print "output:",args.output

  print "Create flat array..."
  flat_data = create_flat_array()
  print "Flat array created..."
  grouped_data = create_grouped_array(flat_data)
  print "Grouped array created... saving to output file"
  counter = 0
  for i in grouped_data.items():
    #print i[1]
    counter += 1
    with open(args.output, 'a') as the_file:
      the_file.write(json.dumps(i[1])+"\n")
    if counter % 1000 == 0:
      print counter
  print "Finished..."
