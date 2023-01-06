from ldif import LDIFParser
import csv
import sys

#ldif = sys.argv[1]
ldif = 'ld.txt'

parser = LDIFParser(open(ldif, "rb"))
list = []

try:
    for dn, record in parser.parse():
        usuario = record['cn'][0]
        uid = record['uid'][0]
        mail = record['mail'][0]
        permisos = record['employeeType']
        list.append([usuario,uid,permisos,mail,permisos])
        
except:
    pass

with open('salida.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(list)