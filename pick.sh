#!/bin/sh
# TODO write script so that it checks if splunk is installed in device
# and also mongodb

sudo su - splunk -c "cd bin; ./splunk start"

sudo systemctl start mongod

python3 src/main.py