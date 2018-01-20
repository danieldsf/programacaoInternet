
class RequestDetails():
	def __init__(self, url, response):
		self.url = url
		self.set_version(response.raw.version)
		
		self.number = response.status_code
		self.text = response.text
		self.response_header = response.headers
		
		self.set_content_lenght(response.content)

	def set_version(self, version):
		self.version = {11: '1.1', 10: '1.0'}[version]

	def set_content_lenght(self, content):
		result = len(content)
		for i in ['KB', 'MB', 'GB']:
			result /= 1024
			output = ''
			if(result < 1024):
				output = '%.2f %s' % (result, i)
				break
		self.content_length = output

	def __str__(self):
		return 'URL: %s\nHTTP version: %s\nStatus Code: %d\nContent Length: %s\nResponse Headers: %s' % (self.url, self.version, self.number, self.content_length, self.response_header)
