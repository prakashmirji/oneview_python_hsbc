from hpOneView.exceptions import HPOneViewException
from hpOneView.oneview_client import OneViewClient
import hpOneView as hpov
import getpass, os
from config_loader import try_load_from_file
pwd=os.getcwd()

config = {
	"ip": "",
	"credentials": {
		"userName": "",
		"password": ""
    },
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

def session_id(oneview_client):
     try:
          sessionId = oneview_client.connection.get_session_id()
          print("Session Id : "+sessionId)
     except HPOneViewException as e:
          print(e)

#getting the password from the user
print("Please Enter HPE OneView Password ")
getPw = getpass.getpass()

# Try load config from a file of appliance 1 (if there is a config file)
config = try_load_from_file(config,'config_3.1.json')
config['credentials']['password'] = getPw

#login into the appliance
con = login(config)

#getting the session id
session_id(con)

#logging out from appliance
logout(con)

# Try load config from a file of appliance 2(if there is a config file)
config = try_load_from_file(config,'config_3.0.json')
config['credentials']['password'] = getPw

#login into the appliance
con = login(config)

#getting the session id
session_id(con)

#logging out from appliance
logout(con)
