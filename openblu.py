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

# Configure this section ^_^
api_token = "Should be secret~"

def check_server(code, url="https://api.intellivoid.info/openblu"):
	id = code
	request_api = {
		"server_id": id,
		"api_key": api_token
	}

	api_response = requests.post(url + "/v1/getServer", request_api)
	json_req = json.loads(api_response.text)
	status = api_response.status_code
	if not int(status) == int(200):
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

	# TODO
	#if not json_req['status'] == "true":
	#	return "dunno"

	payload = json_req['payload']
	id = payload['id']
	host = payload['host_name']
	ip = payload['ip_address']
	score = payload['score']
	ping = payload['ping']
	country = payload['country']
	iso_country = payload['country_short']
	sessions = payload['sessions']
	total_sessions = payload['total_sessions']
	last_updated = payload['last_updated']
	created = payload['created']
	last_updated_formatted = time.strftime("%Y %B %d %H:%M", time.localtime(int(last_updated)))
	created_formatted = time.strftime("%Y %B %d %H:%M", time.localtime(int(created)))

	# Tricky Part
	print("\n\nStarting to export OpenVPN Configuration!\n")
	ref = json_req['ref_code']
	ovpn = payload['openvpn']
	ovpn_output = ovpn['ovpn_configuration']
	file_name = f"openblu_{ref}"
	file = open(f"{file_name}.ovpn", 'w')
	file.write(ovpn_output)
	file.close()
	print("Done!\n\n")

	time.sleep(5)

	full = f"""
VPN Information:
VPN ID: {id}
VPM Host Name: {host}
VPN IP: {ip}
VPN Score: {score}
VPN Country: {country} ({iso_country})
VPN Current Active Sessions: {sessions} sessions
VPN Total Sessions: {total_sessions} sessions
VPN Last Updated (UnFormatted): {last_updated}
VPN Created At (UnFormatted): {created}
VPN Last Updated: {last_updated_formatted}
VPN Created At: {created_formatted}
"""
	print(full)
	return "success"



# check_server("SERVER_ID")

# Example

check_server("33651b4d1c3443a5")
