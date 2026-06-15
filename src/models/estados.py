# modo: "scatter" o "chase", "frightened"
# fase: 0, 1, 2, etc
class Estado:
    def __init__(self):
        self.fase = [
            ("SCATTER", 7),
            ("CHASE", 20),
            ("SCATTER", 7),
            ("CHASE", 20),
            ("SCATTER", 5),
            ("CHASE", 20),
            ("SCATTER", 5),
            ("CHASE", None),
        ]  # cada fase con el tiempo que dura cada una

        self.fase_actual = 0
        self.modo_actual = "SCATTER"
        self.tiempo_fase = 0

    def actualizar(self, dt: float, asustado: bool):
        """ Actualiza el estado de los fantasmas dependiendo del tiempo 
        transcurrido y si están asustados o no.

        Argumentos:
            dt (float): el tiempo transcurrido desde la última actualización
            asustado (bool): Indica si Pac-Man está asustado

        Retorna:
            bool: True si hubo un cambio de fase, False en caso contrario
        """
         
        if asustado:
            return False

        self.tiempo_fase += dt

        duracion = self.fase[self.fase_actual][1]
        if duracion is not None and self.tiempo_fase >= duracion:
            self.fase_actual += 1  # sumo 1 para que pase a la siguiente fase
            self.tiempo_fase = 0  # reseteo el tiempo a 0 cuando empieza la proxima fase

            self.modo_actual = self.fase[self.fase_actual][0]

            return True  # devuelve True si entro al if porque hubo cambio de fase

        return False  # si no entra al if devuelve False porque no hubo cambio de fase

    def reset(self):
        """Reinicia el sistema de estados al comienzo de la secuencia, 
        restaurando la primera fase SCATTER y reiniciando el temporizador interno.
        """
        
        self.fase_actual = 0
        self.modo_actual = "SCATTER"
        self.tiempo_fase = 0

    def obtener_modo(self):  # para que los fantasmas hagan modo = estado.obtener_modo()
        """Obtiene el modo actual del sistema de estados.

        Retorna:
            str: el modo actual del sistema de estados.
        """
        return self.modo_actual
