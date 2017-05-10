from incidencia import Incidencia
from camara import Camara
from listaCamaras import ListaCamaras

class ListaIncidencias:
    lista = []

    def __init__(self, xml, listaCamaras):
        try:
            prueba = xml["Incidencias"]["Incidencia"][0]["Texto"]
            for i in xml["Incidencias"]["Incidencia"]:
                self.lista.append(Incidencia(i["Texto"],
                                    float(i["Posicion"]["Latitud"]),
                                    float(i["Posicion"]["Longitud"]),
                                    i["Identificador"]))
        except:
            try:
                self.lista.append(Incidencia(xml["Incidencias"]["Incidencia"]["Texto"],
                                    float(xml["Incidencias"]["Incidencia"]["Posicion"]["Latitud"]),
                                    float(xml["Incidencias"]["Incidencia"]["Posicion"]["Longitud"]),
                                    xml["Incidencias"]["Incidencia"]["Identificador"]))
            except:
                self.lista = []

        if self.lista is not None:
            try:
                for i in self.lista:
                    arrayPos = 0
                    camaraPos = 0
                    minPos = 100
                    for c in listaCamaras.lista:
                        if abs(i.latitud - c.latitud) + abs(i.longitud - c.longitud) < minPos:
                            minPos = abs(i.latitud - c.latitud) + abs(i.longitud - c.longitud)
                            camaraPos = arrayPos
                        arrayPos = arrayPos + 1
                        i.camara = listaCamaras.lista[camaraPos]
            except:
                arrayPos = 0
                camaraPos = 0
                minPos = 100
                for c in listaCamaras.lista:
                    if abs(self.lista.latitud - c.latitud) + abs(self.lista.longitud - c.longitud) < minPos:
                        minPos = abs(self.lista.latitud - c.latitud) + abs(self.lista.longitud - c.longitud)
                        camaraPos = arrayPos
                    arrayPos = arrayPos + 1
                    self.lista.camara = listaCamaras.lista[camaraPos]

    def nuevos(self, lista, ids):
        #print("Incidencias cogidas: " + str(len(ids)))
        #print("Incidencias nuevas: " + str(len(lista))
        
        if lista is None:
            return []
        elif ids is None:
            return lista
        else:
            nuevos = []
            if isinstance(lista, list) and isinstance(ids, list):
                for i in lista:
                    if i.identificador not in ids:
                        nuevos.append(i)
            elif isinstance(lista, list):
                for i in lista:
                    if i.identificador != ids:
                        nuevos.append(i)
            elif isinstance(ids, list):
                for i in ids:
                    if i != lista.identificador:
                        return lista
            #print("Incidencias filtradas nuevas: " + str(len(nuevos)))
            return nuevos

    def mostrar(self, separador=" --------------------------"):
        try:
            if len(self.lista) > 0:
                for i in self.lista:
                    print(separador)
                    print(i.identificador)
                    print(i.text)
                    print(i.camara.url)
            else:
                print(separador)
                print("No hay incidencias nuevas")
        except:
            if self.lista is not None:
                print(separador)
                print(self.lista.identificador)
                print(self.lista.text)
                print(self.lista.camara.url)
            else:
                print(separador)
                print("No hay incidencias nuevas")
