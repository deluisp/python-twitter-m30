class Incidencia:
    text = None
    latitud = None
    longitud = None
    identificador = None
    camara = None

    def __init__(self, text, latitud, longitud, identificador):
        self.text = text
        self.latitud = latitud
        self.longitud = longitud
        self.identificador = identificador
