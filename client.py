import tkinter
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

def primire():
    while True:
        try:
            mesaj = client_socket.recv(marime).decode("utf8")
            mesaje.insert(tkinter.END, mesaj)
            if mesaj == 'Conexiune refuzată':
                time.sleep(2)
                inchide()
        except OSError:
            break

def trimite_mesaj(event=None):
    mesaj = meu_mesaj.get()
    meu_mesaj.set('')
    client_socket.send(bytes(mesaj, "utf8"))
    if mesaj == '!q':
        client_socket.close()
        top.quit()

def inchide(event=None):
    meu_mesaj.set('!q')
    trimite_mesaj()

top = tkinter.Tk()

mesaje_cadru = tkinter.Frame(top)
meu_mesaj = tkinter.StringVar()
baraDeDerulare = tkinter.Scrollbar(mesaje_cadru)
mesaje = tkinter.Listbox(mesaje_cadru, height=15, width=50, yscrollcommand=baraDeDerulare.set)
baraDeDerulare.pack(side=tkinter.RIGHT, fill=tkinter.Y)
mesaje.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
mesaje.pack()
mesaje_cadru.pack()

camp_intrare = tkinter.Entry(top, textvariable=meu_mesaj)
camp_intrare.bind("<Return>", trimite_mesaj)
camp_intrare.pack()
buton_trimite = tkinter.Button(top, text="Send", command=trimite_mesaj)
buton_trimite.pack()

top.protocol("WM_DELETE_WINDOW", inchide)

host = 'localhost'
port = 9999

marime = 512
adr = (host, port)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(adr)

primeste_fir = Thread(target=primire)
primeste_fir.start()
tkinter.mainloop()
