from requests import post
import multiprocessing as mp
from datetime import datetime
from random import choice
import xmltodict
from config import AUTH

URL_CONSULTA_DOCUMENTO = 'https://iop.gba.gob.ar/servicios/GDEBA/1/SOAP/consultaDocumento?wsdl'

# Consulto el detalle de los gedos
def consultar_detalle_gedo():
    
    gedo = choice([
        'IF-2021-32197594-GDEBA-TESTGDEBA',
        'IF-2021-30397421-GDEBA-TESTGDEBA',
        'IF-2021-26819409-GDEBA-TESTGDEBA',
        ])

    response = post('https://iop.gba.gob.ar/servicios/JWT/1/REST/jwt', auth=AUTH)

    token = response.content.decode('utf-8')
    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'Authorization': f'Bearer {token}'
    }

    payload = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
    <Body>
        <buscarPorNumero xmlns="https://iop.gba.gob.ar/gdeba_consultaDocumento">
            <request xmlns="">
                <assignee>true</assignee>
                <numeroDocumento>{gedo}</numeroDocumento>
                <usuarioConsulta>USERT</usuarioConsulta>
            </request>
        </buscarPorNumero>
    </Body>
    </Envelope>"""

    response = post(URL_CONSULTA_DOCUMENTO, headers=headers, data=payload)
    
    if response:
        response_dic = xmltodict.parse(response.content)['soap:Envelope']['soap:Body']['iop:consultarDocumentoPorNumeroResponse']['response']
        return response_dic
    


if __name__ == '__main__':
    print('#'*130)
    for _ in range(3):
        detalle = consultar_detalle_gedo()
        for key, value in detalle.items():
            print(f'{key}: {value}')
        print('#'*130)