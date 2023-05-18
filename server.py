from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def accept_conexiuni():
    while True:
        client_socket, client_adresa= server.accept()
        print('%s:%s este acum conectat.' % client_adresa)
        client_socket.send(bytes('Introduceți numele și apăsați enter pentru a vă conecta la chat', 'utf8'))
        adrese[client_socket] = client_adresa
        Thread(target=client_comunicare, args=(client_socket,)).start()

def client_comunicare(client_socket):
    nume = client_socket.recv(marime).decode('utf8')
    if nume not in permis_clienti:
        client_socket.send(bytes('Conexiune refuzată', 'utf8'))
        return
    bunvenit = 'Bun venit %s! Pentru a pleca din chat, tastează !q' % nume
    client_socket.send(bytes(bunvenit, 'utf8'))
    mesaj = '%s s-a alăturat chatului!' % nume
    afisare(bytes(mesaj, 'utf8'))
    clienti[client_socket] = nume

    while True:
        mesaj = client_socket.recv(marime)
        if mesaj != bytes('!q', 'utf8'):
            afisare(mesaj, nume + ': ')
        else:
            client_socket.send(bytes('!q', 'utf8'))
            client_socket.close()
            del clienti[client_socket]
            afisare(bytes('%s a parasit conversatia.' % nume, 'utf8'))
            break


def afisare(mesaj, prefix=''):
    for sock in clienti:
        sock.send(bytes(prefix, 'utf-8') + mesaj)

host = 'localhost'
port = 9999
marime = 512
adr = (host, port)
clienti = {}
adrese = {}
permis_clienti = ['tester', 'admin', 'guest']

server = socket(AF_INET, SOCK_STREAM)
server.bind(adr)

server.listen(5)
print('Chat-ul este deschis ...')
handle_connections = Thread(target=accept_conexiuni())
handle_connections.start()
handle_connections.join()
server.close()