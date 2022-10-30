import socket
import threading


host = "127.0.0.1"  #local
port = 1234
host_port = (host, port)
buffer = 1024

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(host_port)
sock.listen()

clients = []
clients = clients[:2]
usernames = []

def handle(client):
    while True:
        try:
            message = client.recv(buffer)
            if message == b'WHO\n':
                list1 = ', '.join(usernames)
                client.send(f'WHO-OK {list1}\n'.encode('utf-8'))
            
            elif b'SEND ' in message:
                message = message.decode('utf-8')
                recipient = message.split()[1]

                if recipient in usernames:
                    message1 = message.replace('SEND ', '')
                    message1 = message1.replace(recipient + ' ', '')
                    if message1 == '\n':
                        client.send(b'BAD-RQST-BODY\n')
                    else:
                        i = usernames.index(recipient)
                        sendToUser = clients[i]

                        username1 = clients.index(client)
                        username1 = usernames[username1]

                        sendToUser.send(b'DELIVERY ' + username1.encode('utf-8') + b' ' + message1.encode('utf-8'))
                else:
                    print('not in usernames')
                    client.send(b'UNKNOWN\n')
            else:
                client.send(b'BAD-RQST-HDR\n')
                

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            usernames.remove(username)
            if username != '':
                print(username + ' has left the server.')
                print(usernames)
            break

def handshake():
    while True:
        client, address = sock.accept()
        print(f'connected with {str(address)}')

        username = client.recv(buffer).decode('utf-8')
        username = username.replace('HELLO-FROM ', '')
        username = username.replace('\n', '')
        clients.append(client)

        if len(clients) > 2:
                client.send(b'BUSY\n')
                clients.remove(client)
                client.close()
                continue

        if username not in usernames:
            client.send(f'HELLO {username}\n'.encode('utf-8'))
            usernames.append(username)
            print(usernames)

        else:    
            client.send('IN-USE\n'.encode('utf-8'))
            clients.remove(client)
            client.close()
            
            continue

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Welcome to Lara and Miguel\'s server...')
handshake()