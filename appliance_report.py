from pprint import pprint

from config_loader import try_load_from_file
from hpOneView.exceptions import HPOneViewException
from hpOneView.oneview_client import OneViewClient
import getpass, os, csv
from hpOneView.resources.resource import ResourceClient
pwd=os.getcwd()

report_file = pwd+os.sep+"appliance_report.csv"
pwd=os.getcwd()


#getting the password from the user
print("Please Enter HPE OneView Password ")
getPw = getpass.getpass()

config = {
	"ip": "",
	"credentials": {
		"userName": "",
		"password": ""
    },
}

def logout():
        # Logout
        try:
                oneview_client.connection.logout(config['credentials'])
                print('Logged out of : '+config['ip'])
        except:
                print('Logout failed')


# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
config['credentials']['password'] = getPw

try:
    oneview_client = OneViewClient(config)
except HPOneViewException as e:
    print("OneView Client Connection Establishment Failed, Please check")

#output file with headers
fp= open (report_file,"w+")
fp.write("firmware_name"+",API_version"+",build"+",compatibility"+",major"+",minor"+",applianceVersion"+",modelNumber"+",platformType"+",revision"+",serialNumber"+"\n")

baselineArray = []

#getting the firmware
all_firmwares = oneview_client.firmware_drivers.get_all()
for firmware in all_firmwares:
        baselineArray.append(firmware['baselineShortName'])

#getting api version
get_version = oneview_client.connection.get_by_uri('/rest/version')
version = get_version['currentVersion']

#appliance details
applianceInfo = oneview_client.connection.get('/rest/appliance/nodeinfo/version')
build = applianceInfo['build']
compatibility = applianceInfo['compatibility']
major = applianceInfo['major']
minor = applianceInfo['minor']
software = applianceInfo['softwareVersion']
modelNumber = applianceInfo['modelNumber']
platformType = applianceInfo['platformType']
revision = applianceInfo['revision']
serialNumber = applianceInfo['serialNumber']

fp.write(str(baselineArray)+","+str(version)+","+str(build)+","+str(compatibility)+","+str(major)+","+str(minor)+","+str(software)+","+str(modelNumber)+","+str(platformType)+","+str(revision)+","+str(serialNumber)+"\n")
print("output file : "+report_file)

logout()
