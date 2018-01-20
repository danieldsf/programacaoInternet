
class RequestFile():
	def __init__(self, filename, response):
		self.filename = filename
		self.set_file_content(response)
		
	def set_file_content(self, text):
		with open(self.filename, 'wb') as fd:
			for chunk in text.iter_content(chunk_size=128):
				fd.write(chunk)