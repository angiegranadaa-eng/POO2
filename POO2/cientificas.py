class Cientifica:
    def __init__(self, nombre, especialidad, dialogo, pos_x, pos_y):
        self.nombre = nombre
        self.especialidad = especialidad
        self.dialogo = dialogo
        self.x = pos_x
        self.y = pos_y

# Creas una lista con las científicas de tu juego
lista_cientificas = [
    Cientifica("Marie Curie", "Física/Química", "¡Hola! Descubrí el radio y el polonio.", 300, 200),
    Cientifica("Ada Lovelace", "Informática", "¡Bienvenido! Creé el primer algoritmo.", 500, 200)
]