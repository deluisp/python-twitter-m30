from camara import Camara

class ListaCamaras:
    lista = []

    def __init__(self, xml):
        self.lista = [None] * (len(xml["Camaras"]["Camara"]))
        x = 0
        for i in xml["Camaras"]["Camara"]:
            self.lista[x] = Camara(i["URL"],
                            float(i["Posicion"]["Latitud"]),
                            float(i["Posicion"]["Longitud"]))
            x = x + 1
