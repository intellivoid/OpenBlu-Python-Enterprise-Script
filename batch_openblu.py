# Copyright © 2019 Haruka Network Development (behalf of Akito Mizukito)
# This file is part of Haruka Network Development (behalf of Akito Mizukito).
#
# This script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License


from datetime import datetime
import json
import requests
import time

from openblu import api_token, check_server

# Config me!
country = "JP"
max = "10"

def batch_server(url="https://api.intellivoid.info/openblu"):
	request_api = {
		"api_key": api_token
	}


	api_response = requests.post(url + "/v1/getServers", request_api)
	json_req = json.loads(api_response.text)
	status = api_response.status_code
	print(status)
	try:
		status = api_response.status_code
		if int(status) == int(401):
			if json_req['message'] == "Authentication is required":
				print("[Error] Authentication is required!\nMake sure you have proper API token!")
				return "401_auth"
		elif int(status) == int(401):
			if json_req['message'] == "Incorrect Authentication":
				print("[Error] Incorrect Authentication!\nMakes ure you have proper API token!")
				return "401_in_auth"
		elif int(status) == int(403):
			if json_req['message'] == "Your access key has been suspended":
				print("[Error] Your access key has been suspended!\nMake sure you have proper API token or contact Intellivoid support if you have any doubt.")
				return "403_susp"
		elif int(status) == int(404):
			if json_req['message'] == "The requested VPN server was not found":
				print("[Error] The requested VPN server was not found. Are you sure your server id is correct?")
				return "404_no"
		else:
			if not int(status) == int(200):

				print("[Error][Unknown] Undefined Error, The system do not know how to deal with this.")

				try:
					code = json_req['code']
					print(f"API Returned Status: {code}")
				except:
					code = json_req['status_code']
					print(f"API Returned Status: {code}")

				print("API Message: " + json_req['message'])
				try:
					print("Ref Code: " + json_req['ref_code'])
				except:
					pass

				return "undefined"

	except:
		pass

	msg = json_req['payload']
	count = int(0)
	for js in msg:
		if js['country_short'] == country:
			if count == int(max):
				return
			else:
				count = int(count) + int(1)

			server_id = js['public_id']
			check_server(server_id)

batch_server()
