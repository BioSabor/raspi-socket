import datetime
import socket
import json

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

class client_api:

    def __init__(self):
        self.config = loadConfig()

        self.url_api = self.config['url_api']
        self.version = self.config['version']
        self.cod_finca = self.config['cod_finca']


    def jsonConvert(self, data): #Falta revisar esto!!!!!
        data = data.replace("(", "").replace(")", "").replace('Return(result="success" dev_id="6718119080000516" total="5897"', '')
        data = data.split('\n')
        data = [i.split("=") for i in data]
        data = {i[0]:i[1] for i in data}
        return data


    def sendDataAPI(self, data):
        print("Enviando datos a la API: " + data)

