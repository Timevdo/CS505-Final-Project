import time

import requests

headers = {
	# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
	# 'Accept': '*/*',
	# 'Accept-Language': 'en-US,en;q=0.5',
	# 'Accept-Encoding': 'gzip, deflate, br',
	'Referer': 'https://www.govinfo.gov/',
	'Content-Type': 'application/json',
	'X-Api-Key': 'I3F45YNciElmKqy2vYiSm0OIWs5zTwo5DZZQ2oUm',
	'Origin': 'https://www.govinfo.gov',
	'DNT': '1',
	'Connection': 'keep-alive',
	'Sec-Fetch-Dest': 'empty',
	'Sec-Fetch-Mode': 'cors',
	'Sec-Fetch-Site': 'cross-site',
	# Requests doesn't support trailers
	# 'TE': 'trailers',
}

json_data = {
	'user': {
		'first_name': 'Ezra',
		'last_name': 'Newman',
		'email': f'govinfoall@ezranewman.com',
		'terms_and_conditions': True,
		'registration_source': 'govinfo-api',
	},
	'options': {
		'example_api_url': 'https://api.govinfo.gov/collections?api_key={{apiKey}}',
		'contact_url': 'https://www.github.com/usgpo/api/issues',
		'site_name': 'Govinfo',
		'send_welcome_email': True,
		'email_from_name': 'Govinfo API team',
		'verify_email': False,
	},
}
while True:
	response = requests.post('https://api.data.gov/api-umbrella/v1/users.json', headers=headers, json=json_data)

	if response.status_code == 201:
		print(f"Successfully created API key")
	else:
		print(f"Failed to create API key")
		print(response.text)
		break

	time.sleep(1)
