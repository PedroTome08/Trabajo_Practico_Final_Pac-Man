import pygame

# mapa = grilla de tiles, cada tile tiene un tipo (pared, pasillo, punto, superpunto)


class Mapa:
    def __init__(self, archivo, ancho_pantalla, alto_pantalla):
        self.grilla = []

        with open(archivo) as mapa_txt:
            lineas = mapa_txt.readlines()
        for linea in lineas:
            self.grilla.append(list(linea.strip("\n")))

        self.validar()

        self.columnas = len(self.grilla[0])
        self.filas = len(self.grilla)
        
        HUD_ALTURA = 80

        self.tile = min(
            ancho_pantalla // self.columnas,
            (alto_pantalla - HUD_ALTURA) // self.filas
        )

        self.offset_x = (
            ancho_pantalla - self.columnas * self.tile
        ) // 2

        self.offset_y = (
            (alto_pantalla - HUD_ALTURA)
            - self.filas * self.tile
        ) // 2
        
        
        self.ancho = self.columnas * self.tile
        self.alto = self.filas * self.tile

        self.pacman_inicio_x = ancho_pantalla // 2
        self.pacman_inicio_y = alto_pantalla // 2

        for f in range(self.filas):
            for c in range(self.columnas):
                if self.grilla[f][c] == "P":
                    self.pacman_inicio_x = (
                        self.offset_x + c * self.tile + self.tile // 2
                    )
                    self.pacman_inicio_y = (
                        self.offset_y + f * self.tile + self.tile // 2
                    )
                    self.grilla[f][c] = " "  # limpia ese lugar para que no quede basura


    class MapaInvalido(Exception):
        """Para cuando el archivo del mapa tiene mal formato"""
        pass
    
    def validar(self):
        """
        Verifica que la grilla cargada tenga un formato válido.
        Lanza MapaInvalido con un mensaje descriptivo si algo está mal.
        """
        VALIDOS = {"X", ".", "o", " ", "G", "-", "P", "T"}

        if len(self.grilla) == 0:
            raise self.MapaInvalido("El mapa está vacío: no tiene ninguna fila.")

        ancho = len(self.grilla[0])
        hay_pacman = False
        hay_ghost_house = False

        for nro_fila, fila in enumerate(self.grilla):
            if len(fila) != ancho:
                raise self.MapaInvalido(
                    f"La fila {nro_fila} tiene {len(fila)} columnas; "
                    f"se esperaban {ancho}. Todas las filas deben tener el mismo largo."
                )
            for nro_col, caracter in enumerate(fila):
                if caracter not in VALIDOS:
                    raise self.MapaInvalido(
                        f"Carácter inválido '{caracter}' en fila {nro_fila}, "
                        f"columna {nro_col}. Permitidos: {sorted(VALIDOS)}."
                    )
                if caracter == "P":
                    hay_pacman = True
                elif caracter == "G":
                    hay_ghost_house = True

        if not hay_pacman:
            raise self.MapaInvalido("Falta la posición inicial de Pac-Man ('P').")
        if not hay_ghost_house:
            raise self.MapaInvalido("Falta la ghost house ('G').")

    def dibujar(self, pantalla):
        """
        Dibuja el mapa en la pantalla, recorriendo la grilla y dibujando cada tile según su tipo.
        Argumentos: pantalla: superficie de pygame donde se dibuja el mapa.
        Retorna: None
        """
        t = self.tile
        for fila in range(len(self.grilla)):
            for columna in range(len(self.grilla[fila])):
                tile = self.grilla[fila][columna]
                x = self.offset_x + columna * t
                y = self.offset_y + fila * t

                # dibujo cada tile con su tipo

                if tile == "X":
                    pygame.draw.rect(pantalla, "blue", pygame.Rect(x, y, t, t))
                elif tile == "o":
                    # power pellet
                    pygame.draw.circle(
                        pantalla, "white", (x + t // 2, y + t // 2), 5
                    )  # + t//2 para centrar el circulo en el tile
                elif tile == "G":
                    # interior de la ghost house
                    pygame.draw.rect(pantalla, "black", pygame.Rect(x, y, t, t))
                elif tile == ".":
                    # punto
                    pygame.draw.circle(
                        pantalla, "white", (x + t // 2, y + t // 2), 2
                    )  # + t//2 para centrar el punto en el tile
                elif tile == " ":
                    # pasillo vacio
                    pygame.draw.rect(pantalla, "black", pygame.Rect(x, y, t, t))
                elif tile == "T":
                    # tunel lateral
                    pygame.draw.rect(pantalla, "black", pygame.Rect(x, y, t, t))
                elif tile == "-":
                    # puerta de la ghost house
                    pygame.draw.line(
                        pantalla, "purple", (x, y + t // 2), (x + t, y + t // 2), 3
                    )  # + t//2 para centrar la linea en el tile
                elif tile == "P":
                    pass
                    # posicion inicial de pacman

    def pasillo_pixel(self, x, y):
        """
        Verifica si las coordenadas (x, y) corresponden a un pasillo o espacio transitable en el mapa.
        Argumentos: x: coordenada horizontal en píxeles, y: coordenada vertical en píxeles.
        Retorna: True si es un pasillo o espacio transitable,
        """
        col = int((x - self.offset_x) // self.tile)
        fil = int((y - self.offset_y) // self.tile)

        if 0 <= fil < self.filas and 0 <= col < self.columnas:
            celda = self.grilla[fil][col]
            return celda == 'X' or celda == 'G' or celda == '-'  # pacman no entra a la casa

        return False

    def quedas_puntos(self):
        """
        Verifica si aún quedan puntos o superpuntos en el mapa.
        Argumentos: None
        Retorna: True si aún quedan puntos o superpuntos, False si no queda ninguno
        """

        for fila in self.grilla:
            if "." in fila or "o" in fila:
                return True  # todavía hay comida
        return False  # no hay más comida, el jugador gana
