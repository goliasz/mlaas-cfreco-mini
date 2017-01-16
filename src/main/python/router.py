
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

from flask import Flask, jsonify, request, Response, abort
from functools import wraps

import json
import time
import requests
import os
import memcache

import threading
import Queue

#from __future__ import absolute_import, unicode_literals
from cf_recommender.recommender import Recommender

C_QUERY_CNT_KEY = "query_cnt"
C_QUERY_RESP_EMPTY_CNT_KEY = "qresp_empty"
C_QUERY_RESP_OK_CNT_KEY = "qresp_ok"
C_TRAIN_CNT_KEY = "train_cnt"

app = Flask(__name__)

cf_settings = {
    # redis
    'expire': 3600 * 24 * 30,
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    },
    # recommendation engine settings
    'recommendation_count': 10,
    'recommendation': {
        'update_interval_sec': 600,
        'search_depth': 100,
        'max_history': 1000,
    },
}

print("Connection to MemCached")
mc = memcache.Client(['localhost:11211'], debug=0)

recommendation = Recommender(cf_settings)

train_queue = Queue.Queue()

class TrainingWorker(threading.Thread):
  #
  def __init__ (self, q):
    self.q = q
    self.reco = Recommender(cf_settings)
    threading.Thread.__init__ (self)
  #
  def run(self):
    while True:
      msg = self.q.get()
      user_id = msg.get("user_id")
      buy_items = msg.get("items")
      for item_id in buy_items:
        self.reco.register(item_id)
      self.reco.like(user_id, buy_items)
      #
      self.q.task_done()
      if self.q.empty():
        break

def inc_cnt(p_key):
    qcnt = mc.get(p_key)
    if not qcnt:
      qcnt = 0
    qcnt += 1
    mc.set(p_key,qcnt,time=7200)

def check_auth(username, password):
    return username == 'token' and password == 'unused'

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 403,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# Router
@app.route('/api/v1.0/router', methods=['POST'])
def set_router_cxt():
  ##
  ret = {"status":"success"}
  #
  time0 = int(time.time()*1000)
  latencykey = 'latency'
  #
  try:
    ##
    message = request.json
    #print message

    # Flush All Training
    try:
      if message.get("rtype","") == 'flush_training':
        latencykey = "latency_"+message.get("rtype","")
        #
        ret["status"] = "success"
        os.system("redis-cli flushall")        
    except Exception, Argument:
      me = "[1] Unexpected Error! "+Argument.message
      print me
      ret["status"] = "error"
      ret["status_reason"] = me
    
    # Service sequence
    try:
      if message.get("rtype","") == 'service':
        latencykey = "latency_"+message.get("rtype","")
        #
        ret["status"] = "error"
        ret["status_reason"] = "Not implemented!"
    except Exception, Argument:
      me = "[1] Unexpected Error! "+Argument.message
      print me  
      ret["status"] = "error"
      ret["status_reason"] = me

    # Train sequence - cf reco
    try:
      if message.get("rtype","") == 'train': 
        latencykey = "latency_"+message.get("rtype","")
        #
        ret["status"] = "success"

        train_queue.put(message)
        train_thread = TrainingWorker(train_queue)
        train_thread.start()        

        #user_id = message.get("user_id")
        #buy_items = message.get("items")
        #for item_id in buy_items:
        #  recommendation.register(item_id)
        #recommendation.like(user_id, buy_items)
        #
        inc_cnt(C_TRAIN_CNT_KEY)        
    except Exception, Argument:
      me = "[2] Unexpected Error! "+Argument.message
      print me
      ret["status"] = "error"
      #ret["status_reason"] = "Unexpected Error!"
      ret["msg"] = me

    # Query sequence - cf reco
    try:
      if message.get("rtype","") == 'query':
        latencykey = "latency_"+message.get("rtype","")
        #
        result = []
        if message.get("items"):
          items = message.get("items")
          #
          itmap = {}
          for item_id in items:
            res0 = recommendation.get(item_id, count=int(message.get("size")))
            for r in res0:
              val = itmap.get(r, 0.0)
              itmap[r] = val + 1.0
          #
          result0 = []
          for key, value in itmap.items():
            #result.append({key:value})
            result0.append({"item":key,"rank":value})
          result0 = sorted(result0, key=lambda k: k["rank"] )
          result0 = result0[-int(message.get("size")):]
          #
          result = []
          for r1 in result0:
            result.append({r1.get("item"):r1.get("rank")})      
        else:
          # We need "item_id" and result "size"   
          result = recommendation.get(message.get("item_id"), count=int(message.get("size")))
          #
        ret["status"] = "success"
        ret["payload"] = result

        inc_cnt(C_QUERY_CNT_KEY)
        if len(result)>0:
          inc_cnt(C_QUERY_RESP_OK_CNT_KEY)
        else:
          inc_cnt(C_QUERY_RESP_EMPTY_CNT_KEY)
    except Exception, Argument:
      em = "[3] Unexpected Error! "+Argument.message
      print em
      ret["status"] = "error"
      ret["status_reason"] = em
      #ret["msg"] = em

    mc.set("message_"+message.get("rtype",""),message,time=7200)
    mc.set("response_"+message.get("rtype",""),ret,time=7200)
  except Exception, Argument:
    em = "[0] Fatal Error! "+Argument.message
    ret["status"] = "fatal error"
    ret["status_reason"] = em
    #ret["msg"] = em

  time1 = int(time.time()*1000)
  latency = time1 - time0

  mc.set(latencykey,{"latency":latency}, time=7200)

  return jsonify(ret)  

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
