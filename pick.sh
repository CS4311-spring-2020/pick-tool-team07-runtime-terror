#!/bin/sh
# TODO write script so that it checks if splunk is installed in device
# and also mongodb

if dpkg-query --list | grep -i splunk > /dev/null
then 
    echo "Starting Splunk"
    sudo su - splunk -c "cd bin; ./splunk start"
else   
    # Install
    echo "Splunk was not found in this system. Installing Splunk..."
    # wget -O splunk-8.0.3-a6754d8441bf-linux-2.6-amd64.deb 'https://www.splunk.com/bin/splunk/DownloadActivityServlet?architecture=x86_64&platform=linux&version=8.0.3&product=splunk&filename=splunk-8.0.3-a6754d8441bf-linux-2.6-amd64.deb&wget=true'
    # dpkg -i splunk-8.0.3-a6754d8441bf-linux-2.6-amd64.deb

    # echo "Splunk installed... Starting Splunk"
    # sudo su - splunk -c "cd bin; ./splunk start"
fi

if which mongod > /dev/null
then
    echo "Mongodb detected starting mongo..."
    sudo systemctl start mongod
else
    echo "Mongodb not found. Installing mongo"
    # TODO
fi

python3 src/main.py