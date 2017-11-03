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
    "ip": "",
    "credentials": {
        "userName": "administrator",
        "password": ""
    },
    "templateName": "",
    "targetApplianceIP": ""

}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
config['credentials']['password'] = entered_password
source_ip = config['ip']

def login(config):
    try:
        oneview_client = OneViewClient(config)
        return oneview_client
    except HPOneViewException as e:
        print("OneView Client Connection Establishment Failed, Please check")
        exit()

def logout(oneview_client):
        # Logout
        try:
                oneview_client.connection.logout(config['credentials'])
                print('\nLogged out of : '+config['ip'])
        except:
                print('\nLogout failed')

def get_template_from_source_OV(oneview_client,name):
    print("\nGet a server profile template from source OV : " + name)
    template_response = oneview_client.server_profile_templates.get_by_name(name)
    if template_response:
        server_hardware_type_response = oneview_client.server_hardware_types.get(template_response['serverHardwareTypeUri'])
        server_hardware_type_name = server_hardware_type_response['name']
        if template_response['firmware']['manageFirmware'] == True:
            firmware_uri = template_response['firmware']['firmwareBaselineUri']
            firmware_response = oneview_client.firmware_drivers.get(firmware_uri)
            firmware_name = firmware_response['name']
        elif template_response['firmware']['manageFirmware'] == False:
            firmware_name = None
    else:
        print(name +" : template is not found!")
    return firmware_name,server_hardware_type_name,template_response

#check resources like hardware type, firmware in target OV
def check_resources_in_target_OV(oneview_client,server_hardware_type_name,firmware_name):
    firmware_list = []
    server_hardware_type_list = []
    all_firmwares = oneview_client.firmware_drivers.get_all()
    for firmware in all_firmwares:
        firmware_list.append(firmware['name']) 
    server_hardware_types = oneview_client.server_hardware_types.get_all()
    for SH_type in server_hardware_types:
        server_hardware_type_list.append(SH_type['name'])
    if (firmware_name != None):
        if (firmware_list) and (firmware_name in firmware_list):
            firmware_status = True
            firmware_response = oneview_client.firmware_drivers.get_by('name', firmware_name)[0]
            target_firmware_uri = firmware_response['uri']        
        else:
            firmware_status = False
            target_firmware_uri = None
    else:
        firmware_status = "no firmware"
        target_firmware_uri = None
    if (server_hardware_type_list != None) and (server_hardware_type_name in server_hardware_type_list):
        SH_type_status = True
        SH_response = oneview_client.server_hardware_types.get_by('name',server_hardware_type_name)[0]
        SH_uri = SH_response['uri']
    else:
        SH_type_status = False
        SH_uri = None

    return firmware_status,SH_type_status,SH_uri,target_firmware_uri
  
try:
    config['ip'] = source_ip
    source_oneview_client = login(config)
    print("\nconnected to the SOURCE appliance :"+ source_ip)    
    for name in config['templateName']:
        config['ip'] = source_ip
        firmware_name,server_hardware_type_name,template_body = get_template_from_source_OV(source_oneview_client,name)
        for ip in config['targetApplianceIP']:
            config['ip'] = ip
            oneview_client = login(config)
            print("\nconnected to the TARGET appliance : " + ip)
            firmware_status,SH_type_status,SH_uri,firmware_uri = check_resources_in_target_OV(oneview_client,server_hardware_type_name,firmware_name)
            if (firmware_status == False) or (SH_type_status == False):
                print("\nERROR : the resources doesn't match in the target OV for the template : " + name)
                logout(oneview_client)
                break
            elif (firmware_status == True) or (SH_type_status == True): 
                template_body['serverHardwareTypeUri'] = SH_uri
                if firmware_status != "no firmware":
                    template_body['firmware']['firmwareBaselineUri'] = firmware_uri
                print "\nCreating server profile template \'"+name+"\' ...", 
                basic_template = oneview_client.server_profile_templates.create(template_body)    
                if (basic_template['status'] == "OK"):
                    print("[CREATED]")
                else:
                    print(basic_template)
              
            logout(oneview_client)
            print("\n#####################################################\n")
except HPOneViewException as e:
    pprint(e)
    
    

