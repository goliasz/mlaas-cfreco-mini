#!/bin/bash

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

if [ -z ${HEALTH+x} ]; then
  echo "var is unset";
else
  echo "var is set to '$HEALTH'";
  echo $HEALTH > /tmp/H_TARGET
fi

echo "cfreco" > /tmp/H_TYPE
echo $HOSTNAME > /tmp/H_APPL
#echo $HOSTNAME > /tmp/H_APPL_ID
echo $HOSTNAME | sed 's/[^-0-9]*//g' | cut -c 2- > /tmp/H_APPL_ID
echo $HOSTNAME > /tmp/H_ID_SHORT
awk -F'[:/]' '(($4 == "docker") && (lastId != $NF)) { lastId = $NF; print $NF; }' /proc/self/cgroup > /tmp/H_ID

#ls -la /tmp/main-router-touch* > /tmp/H_TOUCH
ps -ef > /tmp/H_PS

