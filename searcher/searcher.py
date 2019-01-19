import requests
from bs4 import BeautifulSoup
######
def download(url):
	response = ''
	try:
		response = requests.get(format_link(url)).text
	except requests.exceptions.RequestException as e:
		print("URL not working")
	finally:
		return response
	
def search(keyword, url, depth):
	#Downloading:
	page = download(url)
	page_sem_tags = BeautifulSoup(page, 'html.parser')
	texto = page_sem_tags.text
	trecho_encontrado = texto.find(keyword)
	#Output:
	print("Origem: " + format_link(url))
	print(show_text(texto, trecho_encontrado, keyword))

	if(depth > 0):
		urls = page_sem_tags.findAll(name = 'a')
		all_links = []
		for i in urls:
			if (i.has_attr("href")):
				if not (i.get("href").startswith("#")):
					all_links.append(format_link(i.get('href'), url))

		for i in all_links:
			search(keyword, i, depth-1)

def format_link(url, url_original = None):
	if url.startswith("http://") or url.startswith("https://"):
		return url
	elif url.startswith("//"):
		return "http:" + url
	elif url.startswith("/"):
		if(url_original == None):
			return "http:/"+url
		elif url_original.endswith("/"):
			return url_original + url[1::]
		else:
			return url_original + url
	elif url[0].isalpha():
		return "http://" + url
	else:
		return url 

def show_text(texto, trecho_encontrado, keyword):
	output = ""
	keyword_size = len(keyword)
	
	#print(trecho_encontrado)
	if(trecho_encontrado < 0):
		output = "Palavra nao encontrada"
	elif(trecho_encontrado < 10):
		output = texto[0:trecho_encontrado+10+keyword_size]
	else:
		output = texto[trecho_encontrado-10:trecho_encontrado+10+keyword_size]
	return output

if __name__ == '__main__':
	search('Brasil', '//www.google.com.br', 1)