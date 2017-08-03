from pprint import pprint

from config_loader import try_load_from_file
from hpOneView.exceptions import HPOneViewException
from hpOneView.oneview_client import OneViewClient
import hpOneView as hpov
import getpass
import sys, os, time, logging, json, csv
from hpOneView.resources.resource import ResourceClient
pwd=os.getcwd()

report_file = pwd+os.sep+"appliance_report.csv"
pwd=os.getcwd()

#logfilepath = pwd + os.sep + 'ServerProfileWithDP_LogFile.log'
#logging.basicConfig(filename=logfilepath, filemode="a", level=logging.INFO)
#logging.info(" "+dat+" "+tim+"BEGIN : Create ServerProfile Script!!!")

# Try load config from a file (if there is a config file)
#config = try_load_from_file(config)

def acceptEULA(con):
	# See if we need to accept the EULA before we try to log in
	con.get_eula_status()
	try:
		if con.get_eula_status() is True:
			print('EULA display needed')
			con.set_eula('no')
	except Exception as e:
		print('EXCEPTION:')
		print(e)

#getting the password from the user
print("Please Enter HPE OneView Password ")
getPw = getpass.getpass()
	
con = hpov.connection("10.54.24.18")
credential = {'userName': "administrator", 'password': getPw}
con.login(credential)
acceptEULA(con)

uri = '/rest/firmware-bundles'
filename = "843216_001_spp_2015.10.0-SPP2015100.2015_0921.6.iso"

response = con.get("/rest/appliance-firmware")
print(response)
