import socket
from Config import Config
from PyQt5 import QtCore
from multiprocessing import Queue
import threading

class Host(QtCore.QThread):
    receiveCallBack = QtCore.pyqtSignal(object)

    def __init__(self, port):
        QtCore.QThread.__init__(self)
        self.HOST = '127.0.0.1'
        self.PORT = port
        self.radi = True
        self.sendQueue = Queue()

    def StopHosting(self):
        self.radi = False

    def SendToClient(self, obj):
        self.sendQueue.put(obj.encode("utf-8"))

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            print("Slusam na portu " + str(self.PORT))
            conn, addr = s.accept()
            with conn:
                tRecv = threading.Thread(target=self.receive, args=(conn,))
                tSend = threading.Thread(target=self.send, args=(conn,))

                tRecv.start()
                tSend.start()
                self.SendToClient(Config.serverWelcomeMsg) #inicijalna poruka. da klijent moze da pocne sekvencu za pocetak gejma

                tRecv.join()
                tSend.join()

    def receive(self, conn):
        while self.radi:
            data = conn.recv(Config.bufferSize)
            self.receiveCallBack.emit(data.decode("utf-8"))

    def send(self, conn):
        while self.radi:
            msg = self.sendQueue.get()
            conn.sendall(msg)



class Client(QtCore.QThread):
    receiveCallBack = QtCore.pyqtSignal(object)

    def __init__(self, remoteAddress, remotePort):
        QtCore.QThread.__init__(self)
        self.remoteHOST = remoteAddress  # The server's hostname or IP address
        self.remotePORT = remotePort  # The port used by the server
        self.radi = True
        self.sendQueue = Queue()

    def StopHosting(self):
        self.radi = False

    def SendToServer(self, obj):
        self.sendQueue.put(obj.encode('utf-8'))

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.remoteHOST, self.remotePORT))

            tRecv = threading.Thread(target=self.receive, args=(s,))
            tSend = threading.Thread(target=self.send, args=(s,))

            tRecv.start()
            tSend.start()

            tRecv.join()
            tSend.join()

    def receive(self, conn):
        while self.radi:
            try:
                data = conn.recv(Config.bufferSize)
                self.receiveCallBack.emit(data.decode('utf-8'))
            except:
                self.receiveCallBack.emit("CONN_ERROR")
                self.radi = False

    def send(self, conn):
        while self.radi:
            msg = self.sendQueue.get()
            conn.sendall(msg)