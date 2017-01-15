#!/bin/bash

# Copyright (C) KOLIBERO Piotr Goliasz - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Piotr Goliasz <piotr.goliasz@kolibero.eu>, December 2015

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

