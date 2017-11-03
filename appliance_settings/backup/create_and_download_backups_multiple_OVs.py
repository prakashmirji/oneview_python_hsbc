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

if not os.path.isdir("./backups"):
	os.makedirs("./backups")

def create_and_download_backup(app_ip):
	# Create a new appliance backup
	print("\n## Create a new appliance backup")
	backup_details = oneview_client.backups.create()
	pprint(backup_details)

	filename = "backups/" + app_ip + "_" + backup_details['id']

	# Download the backup archive
	print("\n## Download the previously created backup archive")
	response = oneview_client.backups.download(backup_details['downloadUri'], filename)
	print(response)

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
config['credentials']['password'] = getPw
address = config['ip']

try:
	for ip in address:
		config['ip'] = ip
		oneview_client = login(config)
		print("creating and downloading backup from the appliance "+config['ip'])
		create_and_download_backup(ip)
		logout(oneview_client)
except HPOneViewException as e:
                pprint(e)
