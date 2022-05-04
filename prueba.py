

from con_socket import client_api


api=client_api()

respuesta = api.sendDataAPI()

print(respuesta[1])