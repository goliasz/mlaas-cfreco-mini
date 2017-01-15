#!/bin/bash

# Copyright (C) KOLIBERO Piotr Goliasz - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Piotr Goliasz <piotr.goliasz@kolibero.eu>, December 2015

base='/Preco/'
prog='src/main/script/routerguni.sh'

if [[ $(pgrep -f '/bin/bash src/main/script/routerguni.sh') ]]; then
   echo $prog+" is running";
else
   echo $prog+" not running, so I must do something";
   # Make live again
   cd $base&&$prog &
fi
