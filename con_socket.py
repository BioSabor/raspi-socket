#Creamos una clase de conexion socket

from urllib import response
import datetime
import socket
import json

from sympy import true

class connection:

    def __init__(self):
        self.config = self.loadConfig()

        self.host = self.config['host']
        self.port = self.config['port']
        self.filePath = self.config['filePath']
        self.filePathRequest = self.config['filePathRequest']
        self.url_api = self.config['url_api']
        self.version = self.config['version']
        self.command_getinfo = self.config['get_info']
        self.command_settime = self.config['set_time']
        self.command_getrecord = self.config['get_record']
        

    def loadConfig(self): #Carga la configuracion
        with open('config.json', 'r') as file:
            self.jsonFile = json.load(file)

        return self.jsonFile

    def send(self, mensaje): #Envia el mensaje al servidor
        self.clearFile() #Limpia el archivo antes de consultar los nuevos datos
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect((self.host, self.port))
        self.cliente.send(mensaje.encode('utf-8'))
        self.response = ""

        while True:
            data = self.cliente.recv(1024)      
            self.response = self.response + data.decode('utf-8') 
            # Comprobar si cadena contiene un ")" para terminar la consulta
            if data.find(b')') != -1:
                break
            
        self.cliente.close()
        print("Conexion cerrada")
        self.writeData(self.response, self.filePathRequest)

        return self.response


    def getRecord(self, writeData=False, sendAPI=False): #Envia petición de registros
        self.clearFile(self.filePath) #Limpia el archivo antes de consultar los nuevos datos
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect((self.host, self.port))
        self.cliente.send(self.command_getrecord.encode('utf-8'))
        self.response = ""

        while True:
            data = self.cliente.recv(1024)      
            self.response = self.response + data.decode('utf-8') 
            # Comprobar si cadena contiene un ")" para terminar la consulta
            if data.find(b')') != -1:
                break
            
        self.cliente.close()
        print("Conexion cerrada")

        if writeData:
            self.writeData(self.response, self.filePath)

        if sendAPI:
            self.sendAPI(self.response)
        return self.response


    def sendAPI(self, data): #Envia los datos al API
        print("Se envian los datos a través de la API", data)
        return True


    def clearFile(self, path): #Limpia el archivo
        with open(path, 'w') as file:
            file.write("")


    def writeData(self, data, path): #Escribe los datos en el archivo
        with open(path, 'a') as file:
            file.write(data)


    def updateTime(self): #Actualiza la hora
        self.comand = self.command_settime
        self.fecha = datetime.datetime.now()
        self.week = self.fecha.weekday() + 1      
        self.fecha = self.fecha.strftime("%Y-%m-%d %H:%M:%S") # Damos formato a la fecha
        self.comand = self.comand.replace("*", self.fecha).replace("#", str(self.week))
        self.send(self.comand)