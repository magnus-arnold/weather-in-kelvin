#! /bin/bash

WEBHOST=services.0x1.org

scp -p app.py search.svg site.css site.html site.js root@$WEBHOST:/var/www/weatherinkelvin-com/
ssh root@$WEBHOST /etc/init.d/uwsgi restart
