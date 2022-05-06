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
                        con.deleteAllRecord()
                        
                        if resp == 1:
                            con.setTime()
                        elif resp == 2:
                            con.initAdmin()

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

        