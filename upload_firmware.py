from pprint import pprint

from config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
import getpass , os
pwd=os.getcwd()
config = {
	"ip": "",
	"credentials": {
		"userName": "",
		"password": ""
    },
	"fileName": ""
}

def login(config):
    try:
        oneview_client = OneViewClient(config)
        print("\nconnected to : "+config['ip'])
        return oneview_client
    except HPOneViewException as e:
        print("OneView Client Connection Establishment Failed, Please check")

def logout(oneview_client):
        # Logout
        try:
                oneview_client.connection.logout(config['credentials'])
                print('Logged out of : '+config['ip'])
        except:
                print('Logout failed')


print("Please Enter HPE OneView Password ")
getPw = getpass.getpass()


# To run this example you must define a path to a valid file
#firmware_path = pwd+os.sep+"843216_001_spp_2015.10.0-SPP2015100.2015_0921.6.iso"


def upload_firmware(firmware_path,oneview_client):
	try:
		# Upload a firmware bundle
		print("\nUpload a firmware bundle")
		firmware_bundle_information = oneview_client.firmware_bundles.upload(firmware_path)
		#print(firmware_bundle_information)
		print("\n Upload successful! Firmware information returned: \n")
		pprint(firmware_bundle_information)
	except HPOneViewException as e:
		pprint(e)

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
config['credentials']['password'] = getPw
fileName = config['fileName']
address = config['ip']
firmware_path = pwd + os.sep + fileName

try:
	for ip in address:
		config['ip'] = ip
		oneview_client = login(config)
		print("spp '"+firmware_path+"' uploading to the appliance "+config['ip'])
		upload_firmware(firmware_path,oneview_client)
		logout(oneview_client)
except HPOneViewException as e:
                pprint(e)
