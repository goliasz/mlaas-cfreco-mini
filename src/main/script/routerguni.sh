#!/bin/bash

# Copyright (C) KOLIBERO Piotr Goliasz - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Piotr Goliasz <piotr.goliasz@kolibero.eu>, December 2015

cd /Preco/src/main/python&&/usr/local/bin/gunicorn --workers 2 --bind 0.0.0.0:5000 routerguni:app
