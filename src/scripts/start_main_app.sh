#!/bin/bash
sleep 5
python3 manage.py makemigrations
python3 manage.py migrate --run-syncdb
/usr/bin/supervisord -c "/etc/supervisor/conf.d/supervisord.conf"