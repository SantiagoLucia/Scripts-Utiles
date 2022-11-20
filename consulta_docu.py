from requests import post
import multiprocessing as mp
from datetime import datetime
from random import choice
import xmltodict
from config import AUTH

# SALIDA = f'consultar_detalle_gedo_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.log'
SALIDA = f'consultar_detalle_gedo.log'
URL_CONSULTA_DOCUMENTO = 'https://iop.gba.gob.ar/servicios/GDEBA/1/SOAP/consultaDocumento?wsdl'


# Definición de Funciones
def listener(q):

    with open(SALIDA, 'w') as f:
        while True:
            m = q.get()
            if m == 'kill':
                break
            f.write(str(m) + '\n')
            f.flush()

# Consulto el detalle de los gedos
def consultar_detalle_gedo(queue):
    
    gedo = choice([
        'IF-2021-32197594-GDEBA-TESTGDEBA',
        'IF-2021-30397421-GDEBA-TESTGDEBA',
        'IF-2021-26819409-GDEBA-TESTGDEBA',
        ])

    response = post('https://iop.gba.gob.ar/servicios/JWT/1/REST/jwt', auth=AUTH)

    token = response.content.decode('UTF-8')
    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'Authorization': f'Bearer {token}'
    }

    payload = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
    <Body>
        <buscarPorNumero xmlns="https://iop.gba.gob.ar/gdeba_consultaDocumento">
            <!-- Optional -->
            <request xmlns="">
                <assignee>true</assignee>
                <numeroDocumento>{gedo}</numeroDocumento>
                <usuarioConsulta>USERT</usuarioConsulta>
            </request>
        </buscarPorNumero>
    </Body>
    </Envelope>"""

    # payload = {
    #     'assignee': True,
    #     'numeroDocumento': gedo,
    #     'usuarioConsulta': 'USERT',
    # }

    response = post(URL_CONSULTA_DOCUMENTO, headers=headers, data=payload)

    # response_dic = xmltodict.parse(response.content)['soap:Envelope']['soap:Body']['iop:consultarDocumentoPorNumeroResponse']['response']
    
    p_name = mp.current_process().name
    tiempo = datetime.now()
    queue.put(f'{tiempo} - {p_name} - {response} -> {response.text}')


if __name__ == '__main__':

    m = mp.Manager()
    q = m.Queue()
    pool = mp.Pool()

    pool.apply_async(listener, args=(q,))

    jobs = [ pool.apply_async(consultar_detalle_gedo, args=(q,)) for _ in range(1) ]

    for _ in jobs:
        _.get()

    q.put('kill')
    pool.close()
    pool.join()