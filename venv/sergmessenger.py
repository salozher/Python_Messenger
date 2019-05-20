# Standard library imports
import sys
import os
from socket import socket as sock
from socket import AF_INET, SOCK_STREAM, SHUT_WR
from threading import Thread
import pickle
import time

# Gui related library import
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSlot

# Local application library import
from design import *
from sendableobject import *


class ManageFile:
    def __init__(self):
        pass

    def send_picture(self):
        try:
            image = QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(*.jpg)")
        except:
            print("Can't open the picture file")
        imagepath = image[0]
        print(imagepath)
        try:
            # self.sending_picture()
            process_sending_picture = Thread(target=SendingPicture(imagepath).sending_picture)
            process_sending_picture.start()
            process_sending_picture.join()
        except:
            print("Image file was not selected.")


class SendingPicture:
    def __init__(self, imagepath):
        self.imagepath = imagepath

    def sending_picture(self):
        f = open(self.imagepath, 'rb')
        f_read = f.read()
        connection = MySendPicConnection()
        paket = SendableObject(SendablePackage().picture_send_to_server(f_read))
        connection.send(paket)
        print("Done Sending")
        connection.shutdown()
        del connection
        f.close()
        print("Complete")


class MySendPicConnection:
    def __init__(self, host = 'localhost', port = 4441):
        self.BUFSIZE = 1024
        self.host = host
        self.port = port
        self.socket = sock(AF_INET, SOCK_STREAM)
        self.PICADDR = (self.host, self.port)
        self.socket.connect(self.PICADDR)

    def set_host(self, host):
        self.host = host

    def set_port(self, port):
        self.port = port

    def send(self, paket):
        self.socket.send(pickle.dumps(paket))

    def shutdown(self):
        self.socket.shutdown(SHUT_WR)


class GetPictureFromTheServer:
    def __init__(self):
        self.BUFSIZE = 1024

    def request_picture_from_server(self):
        print("a new thread started to get a picture from server")
        timestr = time.strftime("%H%M%S")
        buffer_file_name = "buffer_file" + timestr + ".pkl"
        print(buffer_file_name)
        picclient_socket = sock(AF_INET, SOCK_STREAM)
        PICREQUESTADDR = ('localhost', 4442)
        picclient_socket.connect(PICREQUESTADDR)
        buffer_file = open(buffer_file_name, 'wb')
        chunk = picclient_socket.recv(self.BUFSIZE)
        while chunk:
            print("Receiving picture")
            buffer_file.write(chunk)
            chunk = picclient_socket.recv(self.BUFSIZE)
        picclient_socket.close()
        buffer_file.close()
        print("Picture package Data is successfully received")
        ff = open(buffer_file_name, 'rb')
        ff_read = ff.read()
        my_unpickled_data = pickle.loads(ff_read)
        my_paket = SendableObject(my_unpickled_data)
        print(my_paket.get_header())
        picture_file_name = "received_picture_file" + timestr + ".jpg"
        print(picture_file_name)
        pp = open(picture_file_name, 'wb')
        pp.write(my_paket[1])
        print("Receiving Picture from Server is completed")
        PICTUREPATH = picture_file_name
        print(PICTUREPATH)
        pp.close()
        ff.close()
        window.publish_picture(PICTUREPATH)


class ManageConnection:
    def __init__(self):
        self.HOST = 'localhost'
        self.PORT = 4440
        self.BUFSIZE = 1024
        self.ADDR = (self.HOST, self.PORT)
        self.client_socket = sock(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()


    def receive(self):
        while True:
            try:
                data = self.client_socket.recv(self.BUFSIZE)
                if data:
                    try:
                        unpickled_data = pickle.loads(data)
                        my_paket = SendableObject(unpickled_data)
                        my_message_id = (my_paket.get_header())
                        if my_message_id != "Picture":
                            chat_message = (my_paket.get_data())
                            window.textBrowser.append(chat_message)
                        else:
                            my_message_id = "Done getting pic"
                            print("Picturemessahe arrived, starting a new thread to initiate a picture receiving")
                            getting_picture = Thread(target=GetPictureFromTheServer().request_picture_from_server)
                            getting_picture.start()
                            getting_picture.join()

                            print("Picture file request started or buffer overflow")
                    except:
                        print("A message arrived caused an ERROR")
                else:
                    print("No data")
            except:
                print("Connection to server has been broken")
                break

    def send(self, data):
        self.client_socket.send(pickle.dumps(data))


class SergAppGui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnSendText.clicked.connect(self.send_message)
        self.btnSendPicture.clicked.connect(ManageFile.send_picture)
        self.btnExit.clicked.connect(self.exit_app)
        self.scene = QGraphicsScene()
        self.grview = self.picView
        self.connection = ManageConnection()


    def send_message(self):
        messagetext = self.textEdit.toPlainText()
        if messagetext:
            chat_data = ["Chat", messagetext]
            self.connection.send(chat_data)
            self.textEdit.clear()
        else:
            self.textEdit.clear()


    def publish_picture(self, picture_path):
        self.textBrowser.append("Message with Picture arrived")
        w = self.picView.width()
        h = self.picView.height()
        try:
            pixmap = QPixmap(picture_path)
        except:
            print("cannot open file")
        pixmap4 = pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio)
        self.scene.clear()
        self.grview.adjustSize()
        mypixmap = QtGui.QPixmap(pixmap4)
        self.scene.addPixmap(mypixmap)
        self.grview.setScene(self.scene)


    def exit_app(self):
        exit_warning = QMessageBox.question(self, 'Confirm closure', "Do you want to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if exit_warning == QMessageBox.Yes:
                exit_code = "{q}"
                send_exit_code = SendableObject(["Chat", exit_code])
                window.connection.client_socket.send(pickle.dumps(send_exit_code))
                window.connection.client_socket.close()
                del window.connection
                window.close()
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SergAppGui()
    window.show()
    app.exec_()