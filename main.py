import json
from con_socket import socket_connection
from con_socket import client_api 
import pandas as pd
import numpy as np

def checkSentences(resp):
    sentences = json.loads(resp)
    if sentences['data'] != None:
        for sentence in sentences['data']:
            if sentence.get('Sentence') == "1":
                con.setTime()
            elif sentence.get('Sentence') == "2":
                con.initAdmin()
            elif sentence.get('Sentence') == "GetErroresAll()":
                api.typeSendData="error"
                api.sendDataAPI(True)
            elif sentence.get('Sentence') == "GetLogsAll()":
                api.typeSendData="data"
                api.sendDataAPI(True)
            else:
                print(sentence.get('Sentence'))

if __name__ == '__main__':
    con = socket_connection() # Inicializamos la conexión socket
    api = client_api() # Inicializamos el cliente API
    # Traer datos
    try:
        request = con.getRecord(True) # Obtenemos los registros

        # Comprobar si hay datos o no
        if request == "" or 'total="0"' in request:
            print("No hay datos")
             # Mandamos ping a la API
            resp, status = api.dataPing()
            checkSentences(resp)

        else:
            print("Hay datos")
            # Procesamos los datos recibidos
            df = con.processData(request, True) # Procesamos los datos recibidos
            #Vaciar de datos el facial
            
            
            #Intentamos enviar datos a la API
            if con.checkBuffer:
                try:
                    resp, status = api.sendDataAPI()
                    if status==200:
                        print('Enviado correctamente')
                        con.clearBuffer()
                        con.deleteAllRecord()
                        checkSentences(resp)
                    else:                      
                        print('No se han procesado los datos en la api')
                        con.registerError('No se han procesado los datos en la api (Posible error en la ruta de la API)')
                        # Agragar error a log de errores

                except Exception as e:
                    print("Error al enviar datos a la API")
                    print(e)
                    con.registerError(str(e))
                    # Agragar error a log de errores
                #Envia datos a la API
    except Exception as e:
        print('No se ha podido conectar con el facial')
        print(e)
        con.registerError(str(e))