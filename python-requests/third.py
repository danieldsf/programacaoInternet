import re

class RequestLinkArray():
	def __init__(self, url, response):
		self.set_arrays(response)
		self.url = url

	def set_arrays(self, response):
		self.links = self.process_regex(response.text)

	def process_regex(self, str_data):
		self.hrefs = re.findall(r'<a.*?href=(\".*?\").*?>.*?</a>', str(str_data))

	def __str__(self):
		str_output = ''
		for i in range(len(self.hrefs)):
			str_output += "%d - %s\n" % (i+1, self.hrefs[i][1:len(self.hrefs[i])-1:])
		return str_output