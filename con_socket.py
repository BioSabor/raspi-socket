#Creamos una clase de conexion socket

from urllib import response
import datetime

import socket

class conection:
    def __init__(self, host, port, filePath):
        self.host = host
        self.port = port
        self.filePath = filePath

    def send(self, mensaje):
        self.clearFile()
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect((self.host, self.port))
        self.cliente.send(mensaje.encode('utf-8'))
        self.response = ""
        while True:
            data = self.cliente.recv(1024)
               
            self.response = self.response + data.decode('utf-8') 

            #comprobar si cadena contiene un caracter
            if data.find(b')') != -1:
                break
            
        self.cliente.close()
        print("Conexion cerrada")
        return self.response


    def clearFile(self):
        with open(self.filePath, 'w') as file:
            file.write("")

    def writeData(self, data):
        with open(self.filePath, 'a') as file:
            file.write(data)

    def updateTime(self, comand):
        self.comand = comand
        self.fecha = datetime.datetime.now()
        self.week = self.fecha.weekday() + 1     
         
        #formato de fecha
        self.fecha = self.fecha.strftime("%Y-%m-%d %H:%M:%S")
        print(self.week, "      ", self.fecha)

        #self.comand = self.comand.replace("*", self.time).replace("#", self.week)




     