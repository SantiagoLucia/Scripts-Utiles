# para instalar automáticamente chromedriver
import logging
import os

# driver de selenium
from selenium import webdriver
# para modificar las opciones de webdriver en Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#desactiva el log del webdriver manager
logging.getLogger('WDM').setLevel(logging.NOTSET)
os.environ['WDM_LOG'] = "false"

def iniciar_chrome():
    """inicia Chrome con los parametros indicados y devuelve el driver"""
    # instala la version de chromedriver correspondiente
    ruta = ChromeDriverManager(path='./chromedriver').install()
    #OPCIONES DE CHROME:
    options = Options() #instanciar las opciones de Chrome
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--start-maximized") #maximiza la ventana de Chrome
    #options.add_argument("--headless") #ejecutar sin abrir la ventana
    #options.add_argument("--disable-gpu")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3") #no muestre nada en la terminal
    options.add_argument("--allow-running-insecure-content") #desactiva el aviso de contenido no seguro
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--no-proxy-server")
    options.add_argument("--disable-blink-features=AutomationControlled") #evita que selenium sea detectado por el navegador
    #parametros para omitir en el inicio
    exp_opt = [
        'enable-automation',
        'ignore-certificate-errors',
        'enable-logging', # para que no muestre el devtools listening
    ]
    options.add_experimental_option("excludeSwitches", exp_opt)
    #parametros de preferencias
    prefs = {
        "profile.default_content_setting_values.notificatios":2, #notificaciones: 0=preguntar 1=permitir 2=no permitir        
        "credentials_enable_service": False, #para evitar que chrome pregunte si quiero guardar contraseñas
    }
    options.add_experimental_option("prefs", prefs)

    #instanciar el servicio de Chromedriver
    s = Service(ruta)
    #instanciar webdriver de selenium con Chrome
    driver = webdriver.Chrome(service=s, options=options)
    return driver


if __name__ == '__main__':
    driver = iniciar_chrome()