import datetime
import socket
import json
import pandas as pd
import numpy as np
import requests

def loadConfig(): #Carga la configuracion
        with open('config.json', 'r') as file:
            jsonFile = json.load(file)
        return jsonFile

class socket_connection:

    def __init__(self):
        self.config = loadConfig()

        self.host = self.config['host']
        self.port = self.config['port']
        self.filePath = self.config['filePath']
        self.filePathRequest = self.config['filePathRequest']
        self.command_getinfo = self.config['get_info']
        self.command_settime = self.config['set_time']
        self.command_getrecord = self.config['get_record']
        self.filepathLogs = self.config['filepathLogs']
        self.filepathBuffer = self.config['filepathBuffer']
        
        

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

        self.writeData(self.response, self.filePathRequest)

        return self.response


    def getRecord(self, writeData=False): #Envia petición de registros
        if writeData:
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

        

        if writeData:
            self.writeData(self.response, self.filePath)

        return self.response


    def processData(self, data, logs = False): #Procesa los datos recibidos
        file = open(self.filePath, 'r')

        data = []

        for line in file:
            if line != "\n":
                data.append(line)
        file.close()

        columns = ['fecha', 'hora', 'id']

        registros = []

        for reg in range(1,5):
            pos = data[reg][31:].find(' ')

            fech = data[reg][6:16]
            hor = data[reg][17:25]
            iden = data[reg][31:30+pos]
            registros.append([fech, hor, iden])

        df_reg = pd.DataFrame(registros, columns=columns)

        for index, row in df_reg.iterrows():
            buffer = row['fecha'] + ";" + row['hora'] + ";" + row['id'] + "\n"
            self.writeBuffer(buffer)
            if logs:
                self.saveLogs(buffer)

        return df_reg
            

    def checkBuffer(self):
        with open(self.filepathBuffer, 'r') as file:
            data = file.read()
        if data == "":
            return False
        else:
            return True

    def clearFile(self, path): #Limpia el archivo
        with open(path, 'w') as file:
            file.write("")


    def writeData(self, data, path): #Escribe los datos en el archivo
        with open(path, 'a') as file:
            file.write(data)

    def writeBuffer(self, data):
        with open(self.filepathBuffer, 'a') as file:
            file.write(data)

    def clearBuffer(self):
        with open(self.filepathBuffer, 'w') as file:
            file.write("")


    def updateTime(self): #Actualiza la hora
        self.comand = self.command_settime
        self.fecha = datetime.datetime.now()
        self.week = self.fecha.weekday() + 1      
        self.fecha = self.fecha.strftime("%Y-%m-%d %H:%M:%S") # Damos formato a la fecha
        self.comand = self.comand.replace("*", self.fecha).replace("#", str(self.week))
        self.send(self.comand)


    def saveLogs(self, data):
        with open(self.filepathLogs, 'a') as file:
            file.write(data)

class client_api:

    def __init__(self):
        self.config = loadConfig()

        self.url_api = self.config['url_api']
        self.version = self.config['version']
        self.cod_finca = self.config['cod_finca']


    def sendDataAPI(self ):
        #Leer fichero buffer


        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(self.url_api + str(self.cod_finca), data='a', headers=headers)
        return r.text, r.status_code

