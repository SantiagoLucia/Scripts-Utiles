from requests import post
from requests.exceptions import HTTPError
import multiprocessing as mp
from datetime import datetime
import xmltodict
from tqdm import tqdm


SALIDA = f'proceso_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.log'

# URL_GENERACION_EXPEDIENTE = 'https://iop.gba.gob.ar/servicios/GDEBA/1/SOAP/generacionExpediente?wsdl'
# URL_BLOQUEAR_EXPEDIENTE = 'https://iop.gba.gob.ar/servicios/GDEBA/1/SOAP/bloqueoExpediente?wsdl'
# URL_PASE_DESBLOQUEO = 'https://iop.gba.gob.ar/servicios/GDEBA/1/SOAP/generacionPaseExpediente?wsdl'
# URL_TOKEN = 'https://iop.gba.gob.ar/servicios/JWT/1/REST/jwt'
# AUTH_TOKEN = ('ws_gdeba_prod_dpma_testgdeba', 'Ws*Hml68')

URL_GENERACION_EXPEDIENTE = 'https://iop.hml.gba.gob.ar/servicios/GDEBA/1/SOAP/generacionExpediente?wsdl'
URL_BLOQUEAR_EXPEDIENTE = 'https://iop.hml.gba.gob.ar/servicios/GDEBA/1/SOAP/bloqueoExpediente?wsdl'
URL_PASE_DESBLOQUEO = 'https://iop.hml.gba.gob.ar/servicios/GDEBA/1/SOAP/generacionPaseExpediente?wsdl'
URL_TOKEN = 'https://iop.hml.gba.gob.ar/servicios/JWT/1/REST/jwt'
AUTH_TOKEN = ('ws_gdeba_hml_dpma_wstestgdeba', 'dpma*123')
            

def obtener_token():
    try:
        response = post(URL_TOKEN,auth=AUTH_TOKEN)
        response.raise_for_status()
        token = response.content.decode('utf-8')
        return token
    except HTTPError as e:
        print(e)


def generar_expediente(queue):
    try:
        headers = {'Content-Type': 'text/xml; charset=utf-8','Authorization': f'Bearer {obtener_token()}'}
        payload = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
        <Body>
            <generarCaratulaExpediente xmlns="https://iop.gba.gob.ar/gdeba_generacionExpediente">
                <!-- Optional -->
                <request xmlns="">
                    <descripcion>Expediente de prueba. Carece de motivacion administrativa</descripcion>
                    <empresa>false</empresa>
                    <externo>false</externo>
                    <interno>true</interno>
                    <usuario>USERT</usuario>
                    <motivo>Expediente de prueba. Carece de motivacion administrativa</motivo>
                    <motivoExterno>Expediente de prueba. Carece de motivacion administrativa</motivoExterno>
                    <codigoTrata>TEST0001</codigoTrata>
                    <tieneCuitCuil>false</tieneCuitCuil>
                </request>
            </generarCaratulaExpediente>
            </Body>
        </Envelope>"""
        r = post(URL_GENERACION_EXPEDIENTE, headers=headers, data=payload)
        p_name = mp.current_process().name
        tiempo = datetime.now()
        r.raise_for_status()
        queue.put(f'{tiempo} - {p_name} - {r} -> {r.text}') 
        return r
    except HTTPError as e:
        queue.put(f'{tiempo} - {p_name} -> {e}')


def bloquear_expediente(queue, nro_expediente):
    try:
        headers = {'Content-Type': 'text/xml; charset=utf-8','Authorization': f'Bearer {obtener_token()}'}
        payload = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
        <Body>
            <bloquearExpediente xmlns="https://iop.gba.gob.ar/gdeba_bloqueoExpediente">
                <numeroExpediente xmlns="">{nro_expediente}</numeroExpediente>
            </bloquearExpediente>
        </Body>
        </Envelope>"""    
        r = post(URL_BLOQUEAR_EXPEDIENTE, headers=headers, data=payload)
        p_name = mp.current_process().name
        tiempo = datetime.now()
        r.raise_for_status()
        queue.put(f'{tiempo} - {p_name} - {r} -> {r.text}') 
        return r
    except HTTPError as e:
        queue.put(f'{tiempo} - {p_name} -> {e}')


def pasar_expediente(queue, nro_expediente):
    try:
        headers = {'Content-Type': 'text/xml; charset=utf-8','Authorization': f'Bearer {obtener_token()}'}
        payload = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
        <Body>
            <generarPaseExpedienteConDesbloqueo xmlns="http://iop.gba.gob.ar/gdeba_generacionPaseExpediente">
                <!-- Optional -->
                <datosPase xmlns="">
                    <numeroExpediente>{nro_expediente}</numeroExpediente>
                    <esMesaDestino>false</esMesaDestino>
                    <esReparticionDestino>false</esReparticionDestino>
                    <esSectorDestino>false</esSectorDestino>
                    <esUsuarioDestino>true</esUsuarioDestino>
                    <estadoSeleccionado>Tramitación</estadoSeleccionado>
                    <motivoPase>'Expediente de prueba. Carece de motivación administrativa.</motivoPase>
                    <usuarioDestino>USERT</usuarioDestino>
                    <usuarioOrigen>USERT</usuarioOrigen>
                </datosPase>
            </generarPaseExpedienteConDesbloqueo>
        </Body>
        </Envelope>""".encode('utf-8')
        r = post(URL_PASE_DESBLOQUEO, headers=headers, data=payload)
        p_name = mp.current_process().name
        tiempo = datetime.now()
        r.raise_for_status()
        queue.put(f'{tiempo} - {p_name} - {r} -> {r.text}') 
        return r
    except HTTPError as e:
        queue.put(f'{tiempo} - {p_name} -> {e}')
        

def consultar_bloqueo(queue, nro_expediente):
    try:
        headers = {'Content-Type': 'text/xml; charset=utf-8','Authorization': f'Bearer {obtener_token()}'}
        payload = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
        <Body>
            <estaExpedienteBloqueado xmlns="https://iop.gba.gob.ar/gdeba_bloqueoExpediente">
                <numeroExpediente xmlns="">{nro_expediente}</numeroExpediente>
            </estaExpedienteBloqueado>
        </Body>
        </Envelope>"""
        r = post(URL_BLOQUEAR_EXPEDIENTE, headers=headers, data=payload)
        r_dict = xmltodict.parse(r.text)
        esta_bloqueado = r_dict['soap:Envelope']['soap:Body']['iop:isBloqueadoResponse']['return']
        p_name = mp.current_process().name
        tiempo = datetime.now()
        r.raise_for_status()
        queue.put(f'{tiempo} - {p_name} - {nro_expediente} -> bloqueado: {esta_bloqueado}') 
        return r
    except HTTPError as e:
        queue.put(f'{tiempo} - {p_name} -> {e}')


def principal(queue, lista):
    resultado = generar_expediente(queue)
    if resultado:
        r_dict = xmltodict.parse(resultado.text)
        numero_expediente = r_dict['soap:Envelope']['soap:Body']['iop:generarCaratulaExpedienteResponse']['return']
        lista.append(numero_expediente)
        resultado = bloquear_expediente(queue, numero_expediente)
        if resultado:
            pasar_expediente(queue, numero_expediente)


def listener(queue):
    with open(SALIDA, 'w') as file:
        while True:
            message = queue.get()
            if message == 'kill': break
            file.write(str(message) + '\n')
            file.flush()


if __name__ == '__main__':

    with mp.Manager() as manager:
        queue = manager.Queue()
        lista_exped = manager.list()
        
        with mp.Pool() as pool:
            pool.apply_async(listener, args=(queue,))
            lista_procesos = [ pool.apply_async(principal, args=(queue,lista_exped,)) for _ in range(100) ]

            for proceso in tqdm(lista_procesos, total=len(lista_procesos), desc='Principal'):
                proceso.wait()
                
            lista_procesos = [ pool.apply_async(consultar_bloqueo, args=(queue,exp,)) for exp in lista_exped ]
        
            for proceso in tqdm(lista_procesos, total=len(lista_procesos), desc='Consultar bloqueo'):
                proceso.wait()
        
            queue.put('kill')
            pool.close()
            pool.join()