#version V0.0.1
#crear un cliente socket
import socket
import json
import os

def decoTiajes():
    pass

def encodeJson(data):
    return json.dumps(data)

def envio(mensaje):
    #crear un socket
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #conectar al servidor
    cliente.connect(('5.154.54.24', 9922))
    
    #enviar mensaje
    cliente.send(mensaje.encode('utf-8'))
    #recibir respuesta

    while True:
        data = cliente.recv(1024)
        #comprobar si cadena contiene un caracter
        if data.find(b')') != -1:
            print("Finaliza trama")
            break

        addText(data.decode('utf-8'))


    cliente.close()
    print("Conexion cerrada")
  

#añadir texto al final del documento ruta relativa
def addText(text):
    print(text)
    with open('datos.txt', 'a') as file:
        file.write(text)


#borrar contenido de un archivo
def clearFile():
    with open('datos.txt', 'w') as file:
        file.write("")

def loadConfig():
    with open('config.json', 'r') as file:
        return json.load(file)

if __name__ == '__main__':
    clearFile()

    while True:
  
        mensaje = input('Ejecuta el comando:')
        envio('GetRecord(start_time="2000-01-01 00:00:00" end_time="2050-12-31 23:59:59")')