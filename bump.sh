#!/bin/bash
sudo service celeryd-nmtk stop
sudo service apache2 stop
sleep 10
sudo service apache2 start
sudo service celeryd-nmtk start
