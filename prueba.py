import pandas as pd 
import numpy as np

fichero = 'buffer/buffer.txt'

#abrir fichero 
columns = ['fecha', 'hora', 'id']
#Cargar ficher a dataframe with
df = pd.read_csv(fichero, sep=';', names=columns)

#convertir dataframe en json

print(df.to_json(orient='records'))

# file = open(fichero, 'r')

# data = []

# for line in file:
#     if line != "\n":
#         data.append(line.replace('\n', ''))
        
# file.close()


# print(data)