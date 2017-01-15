#!/bin/bash

# Copyright (C) KOLIBERO Piotr Goliasz - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Piotr Goliasz <piotr.goliasz@kolibero.eu>, December 2015

base='/Preco/'
script='src/main/script/health-report.sh'
prog='python src/main/python/health-report.py'

if [[ $(pgrep -f 'python src/main/python/health-report.py') ]]; then
   echo $prog+" is running";
else
   echo $prog+" not running, so I must do something";
   # Make live again
   cd $base&&$script
   cd $base&&$prog
fi
