
# Standard library imports
from socket import socket as sock
from socket import AF_INET, SOCK_STREAM, SHUT_WR
from threading import Thread
import pickle
import time

# Local application library import
from sendableobject import *


PIC2BROADCAST = ""


class MyServer:
    def __init__(self):
        self.clients = {}
        self.addresses = {}
        self.HOST
        self.PORT
        self.BUFSIZE = 2048
        self.ADDR = (self.HOST, self.PORT)
        self.SERVER = sock(AF_INET, SOCK_STREAM)
        self.SERVER.bind(self.ADDR)
        self.SERVERCAPACITY = 5
        self.SERVER.listen(self.SERVERCAPACITY)
        self.SERVERMESSAGE = "Server waiting for connection..."
        print(self.SERVERMESSAGE)

    # Getter and setter for a server hostname
    def get_hostname(self):
        return self.HOST

    def set_hostname(self, new_hostname):
        self.HOST = new_hostname

    # Getter and setter for a server port
    def get_port(self):
        return self.PORT

    def set_port(self, new_port):
        self.PORT = new_port

    # Getter and setter for a buffer size
    def get_buffer_size(self):
        return self.BUFSIZE

    def set_buffer_size(self, new_buffer_size):
        self.BUFSIZE = new_buffer_size

    # Getter and setter for a server capacity (amount of allowed connections)
    def get_server_capacity(self):
        return self.SERVERCAPACITY

    def set_server_capacity(self, new_server_capacity):
        self.SERVERCAPACITY = new_server_capacity

    # Getter and setter for a server message
    def get_server_message(self):
        return self.SERVERMESSAGE

    def set_server_message(self, new_server_message):
        self.SERVERMESSAGE = new_server_message


class ChatManagementServer(MyServer):
    def __init__(self):
        self.PORT = 4440
        self.BUFSIZE = 1024
        self.HOST = 'localhost'
        super().__init__()
        self.SERVERMESSAGE = "Chatserver waiting for connection..."
        self.CHATACCEPT_THREAD = Thread(target=self.accept_incoming_chatconnections)
        self.CHATACCEPT_THREAD.start()


    def get_port(self):
        return self.PORT

    def set_port(self, newport):
        self.PORT = newport


    def accept_incoming_chatconnections(self):
        while True:
            chatclient, chatclient_address = self.SERVER.accept()
            print("CHAT SERVER: %s:%s  has connected." % chatclient_address)
            hello_data = SendableObject(SendablePackage().hello_initial_package())
            chatclient.send(pickle.dumps(hello_data))
            self.addresses[chatclient] = chatclient_address
            Thread(target=self.manage_chatclient, args=(chatclient,)).start()


    def manage_chatclient(self, client):
        initialdata = client.recv(self.BUFSIZE)
        try:
            amy_unpickled_data = pickle.loads(initialdata)
            msg = SendableObject(amy_unpickled_data)
            name = msg.get_data()
            welcome = 'Welcome %s!' % name
            welcome_data = SendableObject(SendablePackage().welcome_package(name))
            if client.recv:
                client.send(pickle.dumps(welcome_data))
                msg = SendableObject(SendablePackage().join_package(name))
                self.chatbroadcast(msg)
                self.clients[client] = name
            else:
                client.close()
                print("Connection with " + client + " has been lost")
        except:
            print("Chat client handle error")
        while True:
            data = client.recv(self.BUFSIZE)
            try:
                unpickled_data = pickle.loads(data)
                msg_recieved = SendableObject(unpickled_data)
                parcel = msg_recieved.get_data()
                if msg_recieved.get_data() != "{q}":
                    broadcast_msg = SendableObject(SendablePackage().chat_package(name, parcel))
                    self.chatbroadcast(broadcast_msg)
                else:
                    client.close()
                    print(self.clients[client] + " left our chat")
                    del self.clients[client]
                    broadcast_exit_message = SendableObject(SendablePackage().chat_exit_package(name))
                    self.chatbroadcast(broadcast_exit_message)
                    break
            except:
                print("Buffer overflow")

    def chatbroadcast(self, msg):
        for sock in self.clients:
            sock.send(pickle.dumps(msg))


class IncomingPictureServer:
    def __init__(self):
        self.clients = {}
        self.addresses = {}
        self.HOST = 'localhost'
        self.PICPORT = 4441
        self.BUFSIZE = 1024
        self.PICADDR = (self.HOST, self.PICPORT)
        self.PICSERVER = sock(AF_INET, SOCK_STREAM)
        self.PICSERVER.bind(self.PICADDR)
        self.PICSERVER.listen(5)
        print("Picserver waiting for connection...")
        self.PICACCEPT_THREAD = Thread(target=self.accept_incoming_picconnections)
        self.PICACCEPT_THREAD.start()


    def get_hostname(self):
        return self.HOST

    def set_hostname(self, newhostname):
        self.HOST = newhostname

    def accept_incoming_picconnections(self):
        while True:
            picclient, picclient_address = self.PICSERVER.accept()
            print("PIC SERVER: %s:%s has connected to send a picture." % picclient_address)
            acceptpicconnect = Thread(target=self.manage_picclient, args=(picclient,))
            acceptpicconnect.start()
            acceptpicconnect.join()

    def manage_picclient(self, client):
        timestr = time.strftime("%H%M%S")
        buffer_file_name = "buffer_file" + timestr + ".pkl"
        print(buffer_file_name)
        try:
            pic_file = open(buffer_file_name, 'wb')
            chunk = client.recv(self.BUFSIZE)
            while chunk:
                # print("Receiving picture")
                pic_file.write(chunk)
                chunk = client.recv(self.BUFSIZE)
            client.close()
            pic_file.close()
            print("Data is successfully received")
            ff = open(buffer_file_name, 'rb')
            ff_read = ff.read()
            my_unpickled_data = pickle.loads(ff_read)
            my_paket = SendableObject(my_unpickled_data)
            print(my_paket.get_header())
            received_picture_file_name = "received_picture" + timestr + ".jpg"
            global PIC2BROADCAST
            PIC2BROADCAST = received_picture_file_name
            pp = open(received_picture_file_name, 'wb')
            pp.write(my_paket[1])
            pp.close()
            ff.close()
            print("Done Receiving Picture")
            broadcast_msg = SendableObject(SendablePackage().picture_package(received_picture_file_name))
            chatserver_running.chatbroadcast(broadcast_msg)
        except:
            print("Picture receiving failed")


class OutgoingPictureServer:
    def __init__(self):
        self.HOST = 'localhost'
        self.PICREQUESTPORT = 4442
        self.BUFSIZE = 1024
        self.PICREQUESTARRD = (self.HOST, self.PICREQUESTPORT)
        self.PICREQUESTSERVER = sock(AF_INET, SOCK_STREAM)
        self.PICREQUESTSERVER.bind(self.PICREQUESTARRD)
        self.PICREQUESTSERVER.listen(5)
        print("PicPUSHserver waiting for connection...")
        self.PICREQUESTACCEPT_THREAD = Thread(target=self.accept_incoming_picrequest_connections)
        self.PICREQUESTACCEPT_THREAD.start()

    def get_hostname(self):
        return self.HOST

    def set_hostname(self, newhostname):
        self.HOST = newhostname

    def accept_incoming_picrequest_connections(self):
        while True:
            picgetclient, picgetclient_address = self.PICREQUESTSERVER.accept()
            print("PIC REQUEST SERVER: %s:%s has connected to GET a picture." % picgetclient_address)
            Thread(target=self.manage_picclient_requestingpic, args=(picgetclient,)).start()

    def manage_picclient_requestingpic(self, client):
        try:
            f = open(PIC2BROADCAST, 'rb')
            f_read = f.read()
            paket = SendableObject(SendablePackage().picture_package(f_read))
            client.send(pickle.dumps(paket))
            client.shutdown(SHUT_WR)
            print("Done Sending")
            f.close()
            print("Complete")
        except:
            print("Picture sending failed")


if __name__ == "__main__":
    chatserver_running = ChatManagementServer()
    getpictureserver_running = IncomingPictureServer()
    pushpictureserver_running = OutgoingPictureServer()