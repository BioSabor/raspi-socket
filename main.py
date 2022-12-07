# coding=utf-8

import json
from con_socket import socket_connection
from con_socket import client_api 
import pandas as pd
import numpy as np

def checkSentences(resp):   
    sentences = json.loads(resp)
    if sentences['data'] != None: 
        for sentence in sentences['data']:
            if sentence['Sentence'] == "1":
                con.setTime()
            elif sentence['Sentence'] == "2":
                con.initAdmin()
            elif sentence['Sentence'] == "GetErroresAll()":
                api.typeSendData="error"
                api.sendDataAPI(isSentence=True)
            elif sentence['Sentence'] == "GetLogsAll()":
                api.typeSendData="data"
                api.sendDataAPI(isSentence=True)
            elif "GetPass" in sentence['Sentence']:
                sentence = sentence['Sentence']
                data = json.loads(sentence[sentence.find('{') : sentence.find('}')+1])        
                ret = con.copyLog_Buffer(data['FechaInicio'], data['FechaFin'])
                if ret:
                    enviaBuffer()
            else:
                print(sentence['Sentence'])


def enviaBuffer(conexionFacial=False):
     #Intentamos enviar datos a la API
    if con.checkBuffer:
        try:     
            statusFacial = 0
            if conexionFacial:
                statusFacial = 1

            resp, status = api.sendDataAPI(status=statusFacial)
            if status==200:
                print('Enviado correctamente')
                con.clearBuffer()
                
                if conexionFacial:
                    con.deleteAllRecord()

                checkSentences(resp)

            elif status==400:
                print('No hay datos en el buffer')
            else:                      
                print('No se han procesado los datos en la api')
                con.registerError('No se han procesado los datos en la api (Posible error en la ruta de la API)')
                # Agragar error a log de errores

        except Exception as e:
            print("Error al enviar datos a la API")
            print(e)
            #con.registerError(str(e))
            # Agragar error a log de errores


if __name__ == '__main__':
    con = socket_connection() # Inicializamos la conexión socket
    api = client_api() # Inicializamos el cliente API

    request = ""
    conexionFacial = False
    # Traer datos del facial
    try:
        request = con.getRecord(True) # Obtenemos los registros
        conexionFacial = True
    except Exception as e:
            print('No se ha podido conectar con el facial')
            print(e)
            con.registerError(str(e))
            resp, status = api.dataPing(0)
            checkSentences(resp)
    try:

        if conexionFacial:
            # Comprobar si hay datos o no
            if request == "" or 'total="0"' in request:
                print("No hay datos")
                resp, status = api.dataPing(1)
                checkSentences(resp)
            else:
                print("Hay datos")
                df = con.processData(request, True) # Procesamos los datos recibidos

        enviaBuffer(conexionFacial)

    except Exception as e:
        print('Error al procesar o enviar datos a la API')
        print(e)
        con.registerError(str(e))
        resp, status = api.dataPing(0)
        checkSentences(resp)