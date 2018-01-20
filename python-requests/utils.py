def clean_url(str_data):
	if(str_data.startswith('http://') or str_data.startswith('https://')):
		return str_data
	return 'http://'+str_data