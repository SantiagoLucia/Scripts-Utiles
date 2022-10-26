from requests import post
from zeep import Settings, Client
from datetime import datetime
from tqdm import tqdm
import sys, logging, time
from config import *

dt = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

logging.basicConfig(
    filename=f"pruebaWS_{dt}.log", 
    format="%(asctime)s - %(message)s", 
    datefmt="%d-%m-%y %H:%M:%S",
    level=logging.INFO
    )

#URL de webservices
url_consultaExpediente = URL_CONSULTA_EXPEDIENTE
url_consultaDocumento = URL_CONSULTA_DOCUMENTO

#Expediente a consultar
expediente = sys.argv[1]

#Definición de Funciones
#Consulto el detalle de los gedos
def consultar_detalle_gedo(nro_gedo, usuario):
    request_data = {
        'request': {
            'assignee': True,
            'numeroDocumento': nro_gedo,
            'usuarioConsulta': usuario
        }
    }
    try:
        response = cliente_gedo.service.buscarPorNumero(**request_data)
        logging.info(response['numeroDocumento'] +'    '+response['motivo'])
    except:
        logging.info(nro_gedo+'    '+'El usuario no tiene permiso.')

print('INICIO DE PROCESO')
logging.info('INICIO DE PROCESO')

#Obtener token
try:
    print('Obteniendo Token.')
    logging.info('Obteniendo Token.')
    response = post(URL_TOKEN, auth=AUTH)
    token = response.content.decode('UTF-8')
except:
    print('No se pudo obtener el token.')
    logging.info('No se pudo obtener el Token - Fin del proceso.')
    sys.exit()


#Creo dos instancias de Cliente para los wsdl
settings = Settings(extra_http_headers={'Content-type': 'application/json',
                'Authorization': 'Bearer ' + token}, strict=False)
cliente_ee = Client(wsdl=url_consultaExpediente, settings=settings)
cliente_gedo = Client(wsdl=url_consultaDocumento, settings=settings)

#Expediente a consultar
request_data = {
    'numeroExpediente': expediente
}

#Obtengo documentos en el expediente y usuario caratulador para consultar los documentos
try:
    print(f'Consultando expediente {expediente}.')
    logging.info(f'Consultando expediente {expediente}.')
    response = cliente_ee.service.consultarExpedienteDetallado(**request_data)
    lista_documentos = response['documentosOficiales']
    usuario_caratulador = response['usuarioCaratulador']
except:
    print(f'Error consultando expediente {expediente}.')
    logging.info(f'Error consultando expediente {expediente}.')
    sys.exit()

#Consultando gedos en expediente, retorno numero y motivo
cant_doc = len(lista_documentos)
print(f'se van a consultar {cant_doc} documentos con usuario {usuario_caratulador}.')
logging.info(f'se van a consultar {cant_doc} documentos con usuario {usuario_caratulador}.')

#Tomo tiempo de inicio de consulta de gedos
t_ini = time.perf_counter()

pbar = tqdm(total=cant_doc, desc='Procesando', ascii=' █')
for gedo in lista_documentos:
    consultar_detalle_gedo(gedo, usuario_caratulador)
    pbar.update(1)

pbar.close()

#Tomo tiempo de consulta de fin y calculo el tiempo total y el promedio
t_fin = time.perf_counter()
t_total = t_fin - t_ini
t_totals = str("%.2f" % t_total) #formateo como string para el log
t_prom = t_total / len(lista_documentos)
t_proms = str("%.2f" % t_prom)

print(f'Tiempo total de consulta de gedos: {t_totals} seg')
logging.info(f'Tiempo total de consulta de gedos: {t_totals} seg')
print(f'Tiempo promedio de consulta por gedo: {t_proms} seg')
logging.info(f'Tiempo promedio de consulta por gedo: {t_proms} seg')
print('FIN DE PROCESO')
logging.info('FIN DE PROCESO')