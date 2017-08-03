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

print("Please Enter HPE OneView Password ")
getPw = getpass.getpass()


# To run this example you must define a path to a valid file
#firmware_path = pwd+os.sep+"843216_001_spp_2015.10.0-SPP2015100.2015_0921.6.iso"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
config['credentials']['password'] = getPw
fileName = config['fileName']
firmware_path = pwd + os.sep + fileName
print("spp '"+firmware_path+"' uploading to the appliance "+config['ip'])
oneview_client = OneViewClient(config)

try:
	# Upload a firmware bundle
	print("\nUpload a firmware bundle")
	firmware_bundle_information = oneview_client.firmware_bundles.upload(firmware_path)
	#print(firmware_bundle_information)
	print("\n Upload successful! Firmware information returned: \n")
	pprint(firmware_bundle_information)
except HPOneViewException as e:
	pprint(e)
