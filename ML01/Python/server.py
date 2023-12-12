import socket
serverSocket = socket.socket()
serverSocket.bind(("0.0.0.0", 1234))
serverSocket.listen(5)
clients = []
while True:
    (clientConnected, clientAddress) = serverSocket.accept()

    clients.append(clientAddress)

    print("Accepted a connection request from %s:%s" %
          (clientAddress[0], clientAddress[1]))

    dataFromClient = clientConnected.recv(1024)

    print(dataFromClient)

    print(clients)

    # dataFromServer = "kết nối đến Server thành công"

    # clientConnected.sendto(dataFromServer.encode('utf-8'), (clientAddress[0], 1234))

    if dataFromClient == b"HelloServer":
        print(clientConnected)
        clientConnected.sendto("Hello ESP32".encode(
            'utf-8'), ("192.168.1.8", 1234))
    elif dataFromClient == b"cc":
        clientConnected.sendto("Hello Macbook".encode('utf-8'), clients[0])
