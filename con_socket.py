import datetime
from operator import truediv
from pickle import TRUE
import socket
import json
from datetime import datetime
import pandas as pd
import subprocess
import numpy as np
from sys import platform
from regex import F
import requests

def loadConfig(): #Carga la configuracion
        with open('config.json', 'r') as file:
            jsonFile = json.load(file)
        try:    
            with open('/boot/private.json', 'r') as file:
                privateJson = json.load(file)
        except:
            with open('private.json', 'r') as file:
                privateJson = json.load(file)
        
        return jsonFile, privateJson
    


class socket_connection:

    def __init__(self):
        self.config, self.configPrivate = loadConfig()

        self.host = self.configPrivate['host']
        self.port = self.configPrivate['port']
        self.apiVersion = self.config['api_version']
        self.filePath = self.config['filePath']
        self.filePathRequest = self.config['filePathRequest']
        self.command_getinfo = self.config['get_info']
        self.command_settime = self.config['set_time']
        self.command_getrecord = self.config['get_record']
        self.filepathLogs = self.config['filepathLogs']
        self.filepathBuffer = self.config['filepathBuffer']
        self.command_deleteReg = self.config['del_allTicaje']
        self.command_initAdmin = self.config['reset_admin']
        self.filepathErrors = self.config['filepathErrorLogs']
        

    def send(self, mensaje, write=False):
        #Envia el mensaje al servidor
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
        if write:
            self.writeData(self.response, self.filePathRequest)

        return self.response

    def deleteAllRecord(self):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect((self.host, self.port))
        self.cliente.send(self.command_deleteReg.encode('utf-8'))
        
        
    def initAdmin(self):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect((self.host, self.port))
        self.cliente.send(self.command_initAdmin.encode('utf-8'))
        
        
    def setTime(self):
        comando = self.command_settime   
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        week = datetime.today().isoweekday()
        
        comando = comando.replace("*", time)
        comando = comando.replace("#", str(week))
        
        print(comando)
        
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect((self.host, self.port))
        self.cliente.send(comando.encode('utf-8'))
        
    

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

        for reg in range(1,len(data)):
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
        try:
            with open(self.filepathBuffer, 'r') as file:
                data = file.read()
            if data == "":
                return False
            else:
                return True
        except Exception as e:
            self.writeData("", self.filepathBuffer)
            return False

    def clearFile(self, path): #Limpia el archivo
        with open(path, 'w') as file:
            file.write("")


    def writeData(self, data, path): #Escribe los datos en el archivo
        with open(path, 'a') as file:
            file.write(data)

    def writeBuffer(self, data):
        with open(self.filepathBuffer, 'a') as file:
            file.write(data)
        self.deleteAllRecord()

    def clearBuffer(self):
        with open(self.filepathBuffer, 'w') as file:
            file.write("")

    def registerError(self, data):
        with open(self.filepathErrors, 'a') as file:
            file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " -> " + data +"\n")

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


    def copyLog_Buffer(self, fechaInicio, fechaFin):
        try:
            df = pd.read_csv(self.filepathLogs, sep=';', names=['fecha', 'hora', 'codigo'])
            df = df.dropna()
            mask = (df['fecha'] >= fechaInicio) & (df['fecha'] <= fechaFin)
            df = df.loc[mask]
            df['codigo'] = df['codigo'].astype('Int64')

            with open(self.filepathBuffer) as file:
                doc = file.read()
                if doc != "" and doc[-1:] != '\n':
                    with open('prueba.txt', 'a') as f:
                        f.write('\n')
            df.to_csv(self.filepathBuffer, index=0, sep=';',mode='a', header=False)
            return True  
        except Exception as e:
            self.registerError(e)
            return False

        

class client_api:

    def __init__(self):
        self.config, self.configPrivate = loadConfig()

        self.url_api = self.configPrivate['url_api']
        #self.url_api_fincas = self.configPrivate['url_api_finca']
        self.version = self.config['version']
        self.cod_finca = self.configPrivate['cod_finca']
        self.filePathBuffer = self.config['filepathBuffer']
        self.columnsBuffer = self.config['columns_buffer']
        self.apiVersion = self.config['api_version']
        self.filepathErrors = self.config['filepathErrorLogs']
        self.filepathLogs = self.config['filepathLogs']
        self.typeSendData = "data"
      
        #Incluimos la versión de la API en la URL
        self.url_api = self.url_api.replace('*', self.apiVersion)
        #self.url_api_fincas = self.url_api_fincas.replace('*', self.apiVersion)

    def sendDataAPI(self, isSentence=False):
        if isSentence:
            headers = {'Content-type': 'text/plain'}
            data = 'Por motivos extraños no se ha podido procesar la solicitud'
            if self.typeSendData == "data":
                with open(self.filepathLogs, 'r') as file:
                    data = file.read()
            else: 
                with open(self.filepathErrors, 'r') as file:
                    data = file.read()
            r = requests.post(self.url_api + str(self.cod_finca) +'/'+ self.typeSendData, data=data, headers=headers)
        else:
            data, ndata = self.processData()
            
            if ndata>0:
                #print('El JSON ES: ', data)
                    
                headers = {'Content-type': 'application/json'}
                #Concatenamos el codigo de finca en la URL API
                r = requests.post(self.url_api + str(self.cod_finca), data=data, headers=headers)
                return r.text, r.status_code
            else:
                print("No hay datos para enviar")
                return None
    def checkTemp(self):
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as file:
                data = file.read()
            return data
        except:
            return "0"

    def dataPing(self):
        headers = {'Content-type': 'application/json'}
        data = {
            "version": self.version,   
        }
        data = json.dumps(data)
            #Concatenamos el codigo de finca en la URL API
        r = requests.post(self.url_api + str(self.cod_finca), data=data, headers=headers)

        if platform == 'linux':
            requests.get(self.url_api+ str(self.cod_finca) +'/temperatura/'+ str(int(self.checkTemp())/1000))
        return r.text, r.status_code

    def processData(self): # Proceso los datos recibidos 
        with open(self.filePathBuffer, 'a+') as file:
            file.write("")
        df = pd.read_csv(self.filePathBuffer, sep=';', names=self.columnsBuffer)
        
        return df.to_json(orient='records'), df.shape[0]
        

         

