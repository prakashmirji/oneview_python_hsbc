# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

from pprint import pprint
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file
import getpass, os

#ask user to enter the appliance password
print('Please enter HPE OneView appliance password :')
entered_password = getpass.getpass();

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
config['credentials']['password'] = entered_password

options = {
    "hostname": config['server_hostname'],
    "username": config['server_username'],
    "password": config['server_password'],
    "licensingIntent": "OneView",
    "configurationState": "Managed"
}

# Set the server_hardware_id to run this example.
# server_hardware_id example: 37333036-3831-4753-4831-30315838524E
server_hardware_id = "34323937-3431-4732-3230-313130364747"

try:
    oneview_client = OneViewClient(config)
    # Get list of all server hardware resources
    print("Get list of all server hardware resources")
    server_hardware_all = oneview_client.server_hardware.get_all()
    print (server_hardware_all)
    for serv in server_hardware_all:
        print('  %s' % serv['name'])

    print(' appliance capacity : %s' % len(server_hardware_all))
except HPOneViewException as e:
    print("OneView client connection establishment failed, please check credentials and try again")
finally:
    oneview_client.connection.logout(config['credentials'])
    print('client logging out of : ' + config['ip'])
