import socket
from Config import Config
from PyQt5 import QtCore
from multiprocessing import Queue
import threading

class Host(QtCore.QThread):
    receiveCallBack = QtCore.pyqtSignal(object)

    def __init__(self, serverAddress, port):
        QtCore.QThread.__init__(self)
        self.HOST = "0.0.0.0" #bind na sve dostupne ip adrese
        self.PORT = port
        self.radi = True
        self.sendQueue = Queue()
        self.recvBufferString = ""

    def StopHosting(self):
        self.radi = False

    def SendToClient(self, obj):
        self.sendQueue.put((obj + Config.network_MessageEnd).encode("utf-8"))

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
                self.SendToClient(Config.network_serverWelcomeMsg) #inicijalna poruka. da klijent moze da pocne sekvencu za pocetak gejma

                tRecv.join()
                tSend.join()

                #da host prekine gejm jer se klijent diskonektovao
                self.receiveCallBack.emit("CONN_ERROR")

    def receive(self, conn):
        while self.radi:
            messageEnd = False

            while not messageEnd:
                try:
                    data = conn.recv(Config.bufferSize).decode("utf-8")
                except:
                    self.receiveCallBack.emit("CONN_ERROR")
                    self.radi = False
                    break
                self.recvBufferString += data
                if Config.network_MessageEnd in self.recvBufferString:
                    messageEnd = True

            entireMessagesReceived = self.recvBufferString.split(Config.network_MessageEnd)


            if self.recvBufferString.endswith(Config.network_MessageEnd): #ovde ce uci ako posle kraja za poruku nema vise podataka
                self.recvBufferString = ""
            else: #ako posle kraja za poruku imaju podaci sledece poruke (ali ne svi) onda ce te podatke sto su ostali da sacuva u bufferu za sledece primanje
                self.recvBufferString = entireMessagesReceived[-1]
                entireMessagesReceived = entireMessagesReceived[:-1]

            for msg in entireMessagesReceived:
                self.receiveCallBack.emit(msg)

    def send(self, conn):
        while self.radi:
            msg = self.sendQueue.get()
            try:
                conn.sendall(msg)
            except:
                self.radi = False
                break



class Client(QtCore.QThread):
    receiveCallBack = QtCore.pyqtSignal(object)

    def __init__(self, remoteAddress, remotePort):
        QtCore.QThread.__init__(self)
        self.remoteHOST = remoteAddress  # The server's hostname or IP address
        self.remotePORT = remotePort  # The port used by the server
        self.radi = True
        self.sendQueue = Queue()
        self.recvBufferString = ""

    def StopHosting(self):
        self.radi = False

    def SendToServer(self, obj):
        self.sendQueue.put((obj + Config.network_MessageEnd).encode('utf-8'))

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
            messageEnd = False

            while not messageEnd:
                try:
                    data = conn.recv(Config.bufferSize).decode("utf-8")
                except:
                    self.receiveCallBack.emit("CONN_ERROR")
                    self.radi = False
                    return

                self.recvBufferString += data
                if Config.network_MessageEnd in self.recvBufferString:
                    messageEnd = True

            entireMessagesReceived = self.recvBufferString.split(Config.network_MessageEnd)

            if self.recvBufferString.endswith(
                    Config.network_MessageEnd):  # ovde ce uci ako posle kraja za poruku nema vise podataka
                self.recvBufferString = ""
            else:  # ako posle kraja za poruku imaju podaci sledece poruke (ali ne svi) onda ce te podatke sto su ostali da sacuva u bufferu za sledece primanje
                self.recvBufferString = entireMessagesReceived[-1]
                entireMessagesReceived = entireMessagesReceived[:-1]

            for msg in entireMessagesReceived:
                self.receiveCallBack.emit(msg)

    def send(self, conn):
        while self.radi:
            msg = self.sendQueue.get()
            conn.sendall(msg)

if __name__ == "__main__":
    #ovo je samo za testiranje
    klijent = True
    adresaServera = "127.0.0.1"
    port = 22233
    buffer = 1000

    if klijent:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((adresaServera, port))
            print("Primio sam od servera " + s.recv(buffer).decode('utf-8'))
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((adresaServera, port))
            s.listen()
            print("Slusam na portu " + str(port))
            conn, addr = s.accept()
            conn.sendall(b'Saljem klijentu, ja sam server')

