#!/bin/bash
sudo service celeryd-nmtk stop
sudo service apache2 stop
>/var/www/nmtk/logs/access.log
>/var/www/nmtk/logs/error.log
>/var/www/nmtk/logs/celeryd-nmtk.log
>/var/www/nmtk/logs/django-debug.log
>/var/www/nmtk/logs/django-request.log
sleep 10
sudo service apache2 start
sudo service celeryd-nmtk start
