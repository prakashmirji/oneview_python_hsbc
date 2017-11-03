Prerequisites
-------------

- OneView Python SDK

  	https://github.com/HewlettPackard/python-hpOneView
  
- Python Script

  	migrate_OV_templates.py
	
  	config_loader.py
  
- Cofiguration File

  	config.json
  
Attributes to be set in  
------------------------

- In `config.json` file


	'''{
		"ip": "172.42.253.230",
		"credentials": {
			"userName": "Administrator"
		},
		"api_version": 500,
		"templateName": ["Example_template","Example_template_2","Example_template_3"],
		"targetApplianceIP": ["172.42.253.231"]
	}'''
	
	where
	
	1. ip -> source appliance IP
	
	2. templateName -> server profile template/s to be migrated
	
	3. targetApplianceIP -> appliance ip/s to which profile templates to be migrated
	
	
	
	Note:
	
		- username and password is assumed to be same for all the OV appliances (source and target/s)
		
		
Command to run the script

-------------------------


	$ python migrate_OV_templates.py
	
	
