from requests import post
import multiprocessing as mp
import json
from datetime import datetime
from random import choice
import xmltodict

SALIDA = f'proceso_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.log'

URL_GENERACION_EXPEDIENTE = 'https://iop.hml.gba.gob.ar/servicios/GDEBA/1/SOAP/generacionExpediente?wsdl'
URL_BLOQUEAR_EXPEDIENTE = 'https://iop.hml.gba.gob.ar/servicios/GDEBA/1/SOAP/bloqueoExpediente?wsdl'
URL_VINCULAR_DOCUMENTOS = 'https://iop.hml.gba.gob.ar/servicios/GDEBA/1/SOAP/documentosOficiales?wsdl'
URL_PASE_DESBLOQUEO = 'https://iop.hml.gba.gob.ar/servicios/GDEBA/1/SOAP/generacionPaseExpediente?wsdl'

# Definición de Funciones
def listener(q):

    with open(SALIDA, 'w') as f:
        while True:
            m = q.get()
            if m == 'kill':
                break
            f.write(str(m) + '\n')
            f.flush()



def generar_expediente(q):
    
    # response = post('https://iop.gba.gob.ar/servicios/JWT/1/REST/jwt',
    #     auth=('ws_gdeba_prod_dpma_testgdeba', 'Ws*Hml68'))

    response = post('https://iop.hml.gba.gob.ar/servicios/JWT/1/REST/jwt',
        auth=('ws_gdeba_hml_dpma_wstestgdeba', 'dpma*123'))

    token = response.content.decode('UTF-8')
    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'Authorization': f'Bearer {token}'
    }

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
    
    r_dict = xmltodict.parse(r.text)
    numero_expediente = r_dict['soap:Envelope']['soap:Body']['iop:generarCaratulaExpedienteResponse']['return']
    
    payload = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
    <Body>
        <bloquearExpediente xmlns="https://iop.gba.gob.ar/gdeba_bloqueoExpediente">
            <numeroExpediente xmlns="">{numero_expediente}</numeroExpediente>
        </bloquearExpediente>
    </Body>
    </Envelope>"""    

    if r.status_code == 200:

        r = post(URL_BLOQUEAR_EXPEDIENTE, headers=headers, data=payload)
        
        if r.status_code == 200:
            q.put(numero_expediente)


def crear_lista_expedientes(cantidad):
    m = mp.Manager()
    q = m.Queue()
    pool = mp.Pool()
    lista = []

    jobs = [ pool.apply_async(generar_expediente, args=(q,)) for _ in range(cantidad) ]
    
    for _ in jobs:
        _.get()

    pool.close()
    pool.join()
    q.put(None)

    while True:
        e = q.get()
        if e == None:
            break
        lista.append(e)
    
    return lista


def vincular_hacer_definitivo(queue, expediente):
    
    gedo = choice([
        'IF-2022-00293934-GDEBA-DIPMJGM',
        'IF-2022-00254380-GDEBA-TESTGDEBA',
        'IF-2022-00245391-GDEBA-TESTGDEBA',
        ])

    # response = post('https://iop.gba.gob.ar/servicios/JWT/1/REST/jwt',
    #     auth=('ws_gdeba_prod_dpma_testgdeba', 'Ws*Hml68'))

    response = post('https://iop.hml.gba.gob.ar/servicios/JWT/1/REST/jwt',
        auth=('ws_gdeba_hml_dpma_wstestgdeba', 'dpma*123'))

    token = response.content.decode('UTF-8')
    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'Authorization': f'Bearer {token}'
    }

    payload = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
        <Body>
            <vincularDocumentosOficiales xmlns="https://iop.gba.gob.ar/gdeba_documentosOficiales">
                <!-- Optional -->
                <request xmlns="">
                    <usuario>USERT</usuario>
                    <numeroExpediente>{expediente}</numeroExpediente>
                    <documentosOficiales>{gedo}</documentosOficiales>
                </request>
            </vincularDocumentosOficiales>
        </Body>
    </Envelope>"""

    r = post(URL_VINCULAR_DOCUMENTOS, headers=headers, data=payload)
    
    p_name = mp.current_process().name
    tiempo = datetime.now()
    queue.put(f'{tiempo} - {p_name} - {r} -> {r.text}')    
    
    if r.status_code == 200:
        payload = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
            <Body>
                <hacerDefinitivosDocumentosOficiales xmlns="https://iop.gba.gob.ar/gdeba_documentosOficiales">
                    <!-- Optional -->
                    <request xmlns="">
                        <numeroExpediente>{expediente}</numeroExpediente>
                        <usuario>USERT</usuario>
                    </request>
                </hacerDefinitivosDocumentosOficiales>
            </Body>
        </Envelope>"""

        r = post(URL_VINCULAR_DOCUMENTOS, headers=headers, data=payload)

        p_name = mp.current_process().name
        tiempo = datetime.now()
        queue.put(f'{tiempo} - {p_name} - {r} -> {r.text}')

        if r.status_code == 200:
            payload = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
                <Body>
                    <generarPaseExpedienteConDesbloqueo xmlns="http://iop.gba.gob.ar/gdeba_generacionPaseExpediente">
                        <!-- Optional -->
                        <datosPase xmlns="">
                            <numeroExpediente>{expediente}</numeroExpediente>
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
            queue.put(f'{tiempo} - {p_name} - {r} -> {r.text}')


if __name__ == '__main__':
    
    m = mp.Manager()
    q = m.Queue()
    pool = mp.Pool()

    lista_exp = crear_lista_expedientes(500)

    pool.apply_async(listener, args=(q,))
    jobs = [ pool.apply_async(vincular_hacer_definitivo, args=(q, nro_exp,)) for nro_exp in lista_exp ]

    for _ in jobs:
        _.get()

    q.put('kill')
    pool.close()
    pool.join()