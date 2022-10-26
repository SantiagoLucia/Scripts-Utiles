######
#BORRAR LA PRIMERA PARTE HASTA # PUESTAINICIAL, sade, gob.ar y la ultima parte
######

from ldif import LDIFParser
import csv
import sys

ldif = sys.argv[1]

parser = LDIFParser(open(ldif, "rb"))
list = []
list.append(['usuario','nombre','permisos'])

for record in parser.parse():
    usuario = record[1]['cn'][0]
    nombre = record[1]['uid'][0]
    employeeType = record[1]['employeeType']
    permisos = [x.replace(',ou=grupos,dc=gob,dc=ar','').replace('ou=','').replace(',,dc=gob,dc=ar','').replace(',dc=gov,dc=ar','').replace(',dc=gob,dc=ar','').replace('or=','') for x in employeeType]
    list.append([usuario,nombre,permisos])

with open('salida.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(list)