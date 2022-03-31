from con_socket import connection as conect

if __name__ == '__main__':
    con = conect()
    con.getRecord()
    print("Terminado")