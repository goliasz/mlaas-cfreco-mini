#!/bin/sh

# Copyright (C) KOLIBERO Piotr Goliasz - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Piotr Goliasz <piotr.goliasz@kolibero.eu>, December 2015

rm /var/run/redis_*.pid
service redis_6379 start

cron &

#/usr/bin/mysqld_safe &

memcached -u www-data &

/bin/bash

