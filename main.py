import con_socket
import json


def loadConfig():
    with open('config.json', 'r') as file:
        config = json.load(file)

    return config['host'], config['port'], config['url_api'], config['filePath'], config['set_time']



if __name__ == '__main__':

    host, port, url_api, filePath, cmd_time = loadConfig()
    con = con_socket.conection(host=host, port=port, filePath=filePath)

    #response = con.send('GetRecord(start_time="2000-01-01 00:00:00" end_time="2050-12-31 23:59:59")')
    #con.writeData(response)
    #con.updateTime(cmd_time)
    print("Terminado")

