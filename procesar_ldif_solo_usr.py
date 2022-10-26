######
#BORRAR LA PRIMERA PARTE HASTA # PUESTAINICIAL, sade, gob.ar y la ultima parte
######

from ldif import LDIFParser
import csv
import sys

ldif = sys.argv[1]

parser = LDIFParser(open(ldif, "rb"))
list = []
list.append(['usuario'])

for record in parser.parse():
    usuario = record[1]['cn'][0]
    list.append([usuario])

with open('salida_usr.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(list)