from con_socket import socket_connection
from con_socket import client_api 
import pandas as pd
import numpy as np

if __name__ == '__main__':
    con = socket_connection() # Inicializamos la conexión socket
    api = client_api() # Inicializamos el cliente API
<<<<<<< HEAD

    # Traer datos
    request = con.getRecord(True) # Obtenemos los registros

    # Comprobar si hay datos o no
    if request == "":
        print("No hay datos")
    else:
        print("Hay datos")
        # Procesamos los datos recibidos
        df = con.processData(request, True) # Procesamos los datos recibidos

        #Intentamos enviar datos a la API
        if con.checkBuffer:
            try:
                resp, status = api.sendDataAPI()
            except Exception as e:
                print("Error al enviar datos a la API")
                print(e)
            #Envia datos a la API



        # Si es correcto
        #Limpiamos buffer

        # Si no es correcto
        #Intentamos despues


    print(df)
    # Si hay datos, guardarlos en local



    # Si todo va bien enviar vaciado de datos

    # Enviar datos a API


    
    # print(request)

    # # Guardar los datos en el archivo
    # con.writeData(request, 'data.txt')
    # # con.writeData(request, "./data.txt")
    # #api.sendDataAPI(api.jsonConvert(request)) # Enviamos los datos a la API
    # print("Terminado")
=======
    request = con.getRecord() # Obtenemos los registros
    #print(request)
    api.sendDataAPI(api.jsonConvert(request)) # Enviamos los datos a la API
    print("Terminado")
    
>>>>>>> 585408f13baa5b4e17770764481a1c682e6a5a10
