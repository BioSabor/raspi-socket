from con_socket import socket_connection
from con_socket import client_api 
import pandas as pd
import numpy as np

if __name__ == '__main__':
    con = socket_connection() # Inicializamos la conexión socket
    api = client_api() # Inicializamos el cliente API

    # Traer datos
    try:
        request = con.getRecord(True) # Obtenemos los registros
        
        
        # Comprobar si hay datos o no
        if request == "":
            print("No hay datos")
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
                        con.clearBuffer()
                    else:                      
                        print('No se han procesado los datos en la api')
                        # Agragar error a log de errores

                except Exception as e:
                    print("Error al enviar datos a la API")
                    print(e)
                    # Agragar error a log de errores
                #Envia datos a la API
    except Exception as e:
        print('No se ha podido conectar con el facial')
        print(e)
        # Agragar error a log de errores
        
        
        
    




        # Si es correcto
        #Limpiamos buffer

        # Si no es correcto
        #Intentamos despues


    # Si hay datos, guardarlos en local



    # Si todo va bien enviar vaciado de datos

    # Enviar datos a API


    
    # print(request)

    # # Guardar los datos en el archivo
    # con.writeData(request, 'data.txt')
    # # con.writeData(request, "./data.txt")
    # #api.sendDataAPI(api.jsonConvert(request)) # Enviamos los datos a la API
    # print("Terminado")
