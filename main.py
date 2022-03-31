from con_socket import socket_connection
from con_socket import client_api 

if __name__ == '__main__':
    con = socket_connection() # Inicializamos la conexión socket
    api = client_api() # Inicializamos el cliente API
    request = con.getRecord() # Obtenemos los registros
    #print(request)
    api.sendDataAPI(api.jsonConvert(request)) # Enviamos los datos a la API
    print("Terminado")
    
#