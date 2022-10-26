import pandas as pd
import sqlalchemy
from config import *

query = """SELECT regexp_replace(DU.MAIL, '[ '||chr(10)||chr(13)||chr(9)||']') AS MAIL, SU.NOMBRE_USUARIO AS USUARIOS
FROM TRACK_GED.SADE_SECTOR_USUARIO SU 
LEFT JOIN CO_GED.DATOS_USUARIO DU ON DU.USUARIO = SU.NOMBRE_USUARIO
WHERE SU.ESTADO_REGISTRO = 1 AND DU.ACEPTACION_TYC = 1
"""

url = BD_CON_STRING
engine = sqlalchemy.create_engine(url)

with engine.connect() as con:
    df = pd.read_sql(query, con=con)

df_agrupado = df.groupby(['mail'], as_index=False).agg({'usuarios': ','.join})
df_agrupado.to_csv('mails.csv', index=False, sep=';')
df_agrupado.to_excel('mails.xlsx', index=False)