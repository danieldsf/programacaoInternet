from tkinter import *
import requests 
from third import RequestLinkArray
from utils import clean_url

def hora_do_show():
	make_request(e1.get())

def make_request(url):
	out['text'] = 'Aguarde...Carregando...'
	response = None
	try:
		response = requests.get(clean_url(url))
	except requests.exceptions.RequestException as e:
    	# catastrophic error. bail.
		out['text'] = 'Erro na Requisicao'

	requestLinkArray = RequestLinkArray(url, response)
	out['text'] = requestLinkArray

###

master = Tk()
master.title("HTTP Requests 3")
master.geometry("500x700")

Label(master, text="Digite uma url: ").grid(row=1,pady=1)
Button(master, text='Hora do Show', command=hora_do_show).grid(row=4, column=1, sticky=W, pady=4)

e1 = Entry(master, width=80)
e1.grid(row=1, column=1)

out = Message(master, text="-/-", width=420)
out.grid(row=6, column=1, sticky=W)

###

if __name__ == '__main__':
	master.mainloop()