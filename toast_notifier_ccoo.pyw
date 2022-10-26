from win10toast import ToastNotifier
import sqlalchemy
import time
from config import *
import pandas as pd

while True:
    url = BD_CON_STRING
    engine = sqlalchemy.create_engine(url)

    with engine.connect() as con:
        query='''
        select
        sum(case when dest.fecha_eliminacion_bandeja is null then 1 end) en_bandeja,
        sum(case when dest.leido is null and dest.fecha_eliminacion_bandeja is null then 1 end) sin_leer,
        sum(case when dest.leido is not null and dest.fecha_eliminacion_bandeja is null then 1 end) leidas
        from
        gedo_ged.ccoo_comunicacion_destino dest
        inner join gedo_ged.ccoo_comunicacion com on dest.id_comunicacion = com.id
        where
        dest.nombre_usuario = 'SPRIVITERA'
        '''
        df = pd.read_sql(query, con=con)
        sin_leer = df.iloc[0][1]
        if sin_leer != 0:
            toaster = ToastNotifier()
            toaster.show_toast('CCOO', "Tiene %s comunicaciones sin leer"%(sin_leer), duration=600, icon_path = 'favicon.ico')
        
        time.sleep(600)