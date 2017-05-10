# IMPORTS
import urllib2 as urlRequest
import urllib2 as urlParse
import urllib as imageRequest
import xmltodict
import time
from datetime import datetime
from datetime import timedelta
import string
import argparse
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import tweepy
import requests
import os


# CLASES PROPIAS
from incidencia import Incidencia
from listaIncidencias import ListaIncidencias
from camara import Camara
from listaCamaras import ListaCamaras
from config import *

# URLS
urlIncidencias = "http://www.mc30.es/components/com_hotspots/datos/incidencias.xml"
urlCamaras = "http://www.mc30.es/components/com_hotspots/datos/camaras.xml"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

# FUNCIONES
def cargarIncidencias():
    reqIncidencias = urlRequest.Request(urlIncidencias, headers = headers)
    reqIncidencias = urlRequest.urlopen(reqIncidencias)
    listaIncidencias = reqIncidencias.read()
    reqIncidencias.close()
    return xmltodict.parse(listaIncidencias)

def cargarCamaras():
    reqCamaras = urlRequest.Request(urlCamaras, headers = headers)
    reqCamaras = urlRequest.urlopen(reqCamaras)
    listaCamaras = reqCamaras.read()
    reqCamaras.close()
    return xmltodict.parse(listaCamaras)

def twitter_api():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def tweet(api, url, message, latitude, longitude):
    filename = 'temp.jpg'
    request = requests.get("http://"+url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        api.update_with_media(filename, status=message, lat=latitude, long=longitude)
        os.remove(filename)
    else:
        print("No se pudo descargar la imagen")

# ARGUMENTOS DEL SCRIPT
parser = argparse.ArgumentParser(description="Muestra el id, descripcion y url de la camara mas cercana de las incidencias producidas en la M30")
parser.add_argument("-s", "--seconds", action="store", type=int, help="Tiempo de actualizacion en segundos, por defecto 10 segundos", dest="tiempo", default=10)
parser.add_argument("-a", "--all", action="store_true", help="Muestra todas las incidencias activas en cada iteracion, por defecto False", required=False, default=False)
results = parser.parse_args()

# CUERPO DEL SCRIPT
camaras = ListaCamaras(cargarCamaras())
incidencias = ListaIncidencias(cargarIncidencias(), camaras)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = twitter_api()

ids = []

while 1:
    
    print("\n// -- " + datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") + " -- //")
    incidencias.mostrar("\n")

    for i in incidencias.lista:
        urlGoogle = "http://www.google.com/maps/place/" + str(i.latitud) + "," + str(i.longitud)
        tweet(api, i.camara.url, i.text + ", " + urlGoogle, i.latitud, i.longitud)
    
    time.sleep(results.tiempo)

    camaras = ListaCamaras(cargarCamaras())

    if results.all:
        del incidencias.lista[:]
        incidencias = ListaIncidencias(cargarIncidencias(), camaras)
    else:
        if isinstance(incidencias.lista, list):
            for i in incidencias.lista:
                ids.append(i.identificador)
        else:
            ids.append(incidencias.lista.identificador)

        incidencias.lista = incidencias.nuevos(ListaIncidencias(cargarIncidencias(), camaras).lista, ids)
