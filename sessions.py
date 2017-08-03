from hpOneView.exceptions import HPOneViewException
from hpOneView.oneview_client import OneViewClient
from pprint import pprint
import getpass, os
from config_loader import try_load_from_file
from hpOneView.resources.resource import ResourceClient
pwd=os.getcwd()

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

#getting the password from the user
print("Please Enter HPE OneView Password ")
getPw = getpass.getpass()

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
config['credentials']['password'] = getPw

try:
    oneview_client = OneViewClient(config)
except HPOneViewException as e:
    print("OneView Client Connection Establishment Failed, Please check")

try:
	print("\nGet all ethernet-networks")
	ethernetNets = oneview_client.ethernet_networks.get_all()
	for net in ethernetNets:
		print(net['name'])
	
	sessionId = oneview_client.connection.get_session_id()
	print("Session Id : "+sessionId)
	
	response = oneview_client.connection.get('/rest/appliance/nodeinfo/version')
	pprint(response)

except HPOneViewException as e:
	print(e)

logout()	
