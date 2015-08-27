#!/bin/bash
sudo service celeryd-nmtk stop
sudo service apache2 stop
sudo truncate -s 0 /var/www/nmtk/logs/access.log
sudo truncate -s 0 /var/www/nmtk/logs/error.log
sudo truncate -s 0 /var/www/nmtk/logs/django-debug.log
sudo truncate -s 0 /var/www/nmtk/logs/django-request.log
sudo truncate -s 0 /var/www/nmtk/logs/celeryd-nmtk.log
sleep 10
sudo service apache2 start
sudo service celeryd-nmtk start
source ../../venv/bin/activate
python ../manage.py discover_tools
