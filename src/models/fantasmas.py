import pygame
import random

DELTAS = {"arriba": (-1, 0), "abajo": (1, 0), "izquierda": (0, -1), "derecha": (0, 1)}


class Fantasma:
    def __init__(self, x, y, nombre, color, puntaje, velocidad):
        self.x = x
        self.y = y
        self.nombre = nombre
        self.color = color
        self.puntaje = puntaje
        self.velocidad = velocidad
        self.asustado = False
        self.tiempo_asustado = 0
        self.muerto = False
        self.saliendo_casa = False

        self.img_der = self.imagen(f"assets/images/{nombre.lower()}_der.png", 24)
        self.img_izq = self.imagen(f"assets/images/{nombre.lower()}_izq.png", 24)
        self.img_asustado = self.imagen("assets/images/asustado.png", 24)
        self.img_muerto = self.imagen("assets/images/ojosfantasmas.webp", 24)
        self.direccion = "izquierda"
        self.destino = None
        self.esquina = (-2, 1)  # placeholder, cambiar

        # cosas de la ghost house
        self.encerrado = False
        self.umbral = 0

        # para el reset
        self.x_inicial = x
        self.y_inicial = y
        self.encerrado_inicial = False

    def es_pared(self, mapa, col: int, fila: int):
        """
        Hace que los fantasmas no puedan atravesar las paredes,
        pero sí el túnel. Además, si el fantasma está muerto o saliendo
        de la casa, puede entrar a la ghost house pero no salir de ella.

        Argumentos:
            mapa: el mapa en el que se verifica
            col (int): columna a verificar
            fila (int): fila a verificar

        Retorna:
            bool: True si la celda es una pared, False en caso contrario
        """

        # para dejar pasar por el tunel
        if 0 <= fila < mapa.filas and (col == -1 or col == mapa.columnas):
            if (
                mapa.grilla[fila][0] == "T"
                or mapa.grilla[fila][mapa.columnas - 1] == "T"
            ):
                return False
        if not (0 <= fila < mapa.filas and 0 <= col < mapa.columnas):
            return True

        celda = mapa.grilla[fila][col]

        # si esta muerto puede entrar a la ghost house
        if self.muerto or self.saliendo_casa:
            return celda == "X"

        return celda == "X" or celda == "G"

    def imagen(self, ruta, tamaño):
        """
        Carga una imagen, le quita el fondo transparente sobrante y la escala al tamaño dado.

        Argumentos:
            ruta (str): la ruta del archivo de imagen,
            tamaño (int): el tamaño al que se quiere escalar la imagen (manteniendo proporciones).

        Retorna: una superficie de Pygame con la imagen procesada.
        """
        img = pygame.image.load(ruta).convert_alpha()
        rect = img.get_bounding_rect()
        img = img.subsurface(rect).copy()
        escala = tamaño / max(rect.width, rect.height)
        nuevo = (int(rect.width * escala), int(rect.height * escala))
        return pygame.transform.scale(img, nuevo)

    def dibujar_fantasmas(self, pantalla):
        """
        Dibuja el fantasma en la pantalla según su estado actual (muerto, asustado o normal) y su dirección.

        Argumentos:
            pantalla (pygame.Surface): la superficie de Pygame donde se dibujará el fantasma.

        Retorna: None. El fantasma se dibuja directamente en la pantalla dada.
        """
        if self.muerto:
            img = self.img_muerto
        elif self.asustado:
            if self.tiempo_asustado <= 2 and int(self.tiempo_asustado * 5) % 2 == 0:
                # parpadeo final: muestro la cara normal en vez del azul
                img = self.img_der if self.direccion == "derecha" else self.img_izq
            else:
                img = self.img_asustado
        elif self.direccion == "derecha":
            img = self.img_der
        else:
            img = self.img_izq
        pantalla.blit(img, (self.x - img.get_width() / 2, self.y - img.get_height() / 2))

    def activar_asustado(self, duracion=6):
        """
        Activa el estado asustado del fantasma durante una duración determinada.

        Argumentos:
            duracion (float): el tiempo en segundos que el fantasma permanecerá asustado. Por defecto es 8 segundos.

        Retorna: None
        """
        self.asustado = True
        self.tiempo_asustado = duracion

    def actualizar_asustado(self, dt):
        """
        Actualiza el estado asustado del fantasma restando el tiempo transcurrido (dt) al tiempo restante de asustado. Si el tiempo restante llega a cero o menos, el fantasma deja de estar asustado.

        Argumentos:
            dt (float): el tiempo transcurrido desde la última actualización, en segundos.

        Retorna: None.
        """
        if self.asustado:
            self.tiempo_asustado -= dt

        if self.tiempo_asustado <= 0:
            self.asustado = False

    def velocidad_actual(self, mapa):
        """
            Calcula la velocidad actual del fantasma según su estado
            y el tipo de celda en la que se encuentra.

        Argumentos:
            mapa: instancia del mapa utilizada para obtener el tamaño
            de los tiles y la celda actual del fantasma.

        Retorna:
            float: velocidad efectiva del fantasma en píxeles por segundo.
        """

        base = 7.5 * mapa.tile
        if self.muerto:
            return base * 1.50
        if self.asustado:
            return base * 0.50
        fila, col = self.tile_actual(mapa)
        if 0 <= fila < mapa.filas and 0 <= col < mapa.columnas:
            if mapa.grilla[fila][col] == "T":
                return base * 0.40
        return base * 0.75

    def reset(self, mapa):
        """
        Restablece el estado inicial del fantasma al perder una vida
        o reiniciar la partida, devolviéndolo a su posición original
        y reiniciando sus atributos temporales.

        Argumentos:
            mapa: mapa del juego.

        Retorna:
            None.
        """

        self.x = self.x_inicial
        self.y = self.y_inicial
        self.direccion = "izquierda"
        self.destino = None
        self.muerto = False
        self.asustado = False
        self.saliendo_casa = False
        self.tiempo_asustado = 0
        self.encerrado = self.encerrado_inicial

    def tile_actual(self, mapa):
        """
        Obtiene la fila y columna de la grilla en la que se encuentra
        actualmente el fantasma a partir de sus coordenadas en píxeles.

        Argumentos:
            mapa: mapa utilizado para convertir coordenadas
            de pantalla a coordenadas de la grilla.

        Retorna:
            tuple[int, int]: fila y columna correspondientes a la posición actual
            del fantasma.
        """
        fila = int(
            (self.y - mapa.offset_y) // mapa.tile
        )  # redondear para abajo y calcular la columna y filas en la grilla (no en pixeles)
        col = int((self.x - mapa.offset_x) // mapa.tile)
        return fila, col

    def tile_dexy(self, x: float, y: float, mapa):
        """
            Convierte unas coordenadas dadas en píxeles a la fila y
            columna equivalentes dentro de la grilla del mapa.

        Argumentos:
            x (float): coordenada horizontal en píxeles.
            y (float): coordenada vertical en píxeles.
            mapa: instancia del mapa utilizada para realizar la conversión.

        Retorna:
            tuple[int, int]: fila y columna correspondientes a las coordenadas
            indicadas.
        """

        fila = int((y - mapa.offset_y) // mapa.tile)
        col = int((x - mapa.offset_x) // mapa.tile)
        return fila, col

    def calcular_centro(self, fila, col, mapa):
        """
            Calcula las coordenadas del centro de una celda específica
            del mapa.

        Argumentos:
            fila (int): fila de la celda.
            col (int): columna de la celda.
            mapa: Instancia del mapa utilizada para obtener el tamaño
            de los tiles y los desplazamientos.

        Retorna:
            pygame.Vector2: vector que contiene las coordenadas del centro de la
            celda indicada.
        """
        x = mapa.offset_x + col * mapa.tile + mapa.tile / 2
        y = mapa.offset_y + fila * mapa.tile + mapa.tile / 2
        return pygame.Vector2(x, y)

    def direccion_vecina(self, mapa, fila, col, direccion):
        """
            Obtiene la celda vecina correspondiente a una dirección
            determinada y devuelve también la dirección opuesta.

        Argumentos:
            mapa: mapa del juego.
            fila (int): fila de la celda actual.
            col (int): columna de la celda actual.
            direccion (str): dirección a evaluar ("arriba", "abajo",
            "izquierda" o "derecha").

        Retorna:
            tuple[int, int, str | None]: una tupla con la fila de la celda vecina,
            la columna de la celda vecina y la dirección opuesta a la indicada o
            None si la dirección es inválida.
        """
        if direccion == "arriba":
            destino_fila = fila - 1
            destino_col = col
            opuesta = "abajo"
        elif direccion == "abajo":
            destino_fila = fila + 1
            destino_col = col
            opuesta = "arriba"
        elif direccion == "derecha":
            destino_fila = fila
            destino_col = col + 1
            opuesta = "izquierda"
        elif direccion == "izquierda":
            destino_fila = fila
            destino_col = col - 1
            opuesta = "derecha"
        else:
            # direccion invalida (ej: camino_a devolvio None): me quedo donde estoy
            destino_fila = fila
            destino_col = col
            opuesta = None
        return destino_fila, destino_col, opuesta

    def proxima_direccion(
        self, mapa, opuesta, fila, col, objetivo
    ):  # para cuando llega al objetivo
        """
        Elige la próxima dirección del fantasma basándose en la distancia al objetivo, evitando la dirección opuesta a la actual y las paredes.
        Argumentos: mapa: el mapa del juego, utilizado para verificar paredes y calcular posiciones.
                    opuesta: la dirección opuesta a la actual del fantasma, que se evitará al elegir la próxima dirección.
                    fila, col: la posición actual del fantasma en términos de fila y columna en el mapa.
                    objetivo: una tupla (fila_objetivo, col_objetivo) que representa la posición objetivo a la que el fantasma se dirige.
        Retorna: La dirección elegida para el próximo movimiento del fantasma, que puede ser "arriba", "abajo", "izquierda" o "derecha", o la dirección opuesta si no hay otras opciones disponibles.
        """
        mejor_dist_dir = [None, None]
        for dir in ["arriba", "izquierda", "abajo", "derecha"]:
            if dir == opuesta:
                continue
            dfil, dcol, _ = self.direccion_vecina(mapa, fila, col, dir)
            if self.es_pared(mapa, dcol, dfil):
                continue
            dist = ((objetivo[0] - dfil) ** 2 + (objetivo[1] - dcol) ** 2) ** 0.5
            if mejor_dist_dir[0] is None or dist < mejor_dist_dir[0]:
                mejor_dist_dir[0] = dist
                mejor_dist_dir[1] = dir
        if mejor_dist_dir[0] == None:
            return opuesta
        else:
            return mejor_dist_dir[1]

    def proxima_direccion_asustado(self, mapa, opuesta, fila, col):
        """
        Elige la próxima dirección del fantasma asustado de manera aleatoria, evitando la dirección opuesta a la actual y las paredes.
        Argumentos: mapa: el mapa del juego, utilizado para verificar paredes y calcular posiciones.
                    opuesta: la dirección opuesta a la actual del fantasma, que se evitará al elegir la próxima dirección.
                    fila, col: la posición actual del fantasma en términos de fila y columna en el mapa.
        Retorna: La dirección elegida para el próximo movimiento del fantasma asustado, que puede ser "arriba", "abajo", "izquierda o "derecha", o la dirección opuesta si no hay otras opciones disponibles.
        """
        opciones = []

        for dir in ["arriba", "izquierda", "abajo", "derecha"]:

            if dir == opuesta:
                continue

            dfil, dcol, _ = self.direccion_vecina(mapa, fila, col, dir)

            if self.es_pared(mapa, dcol, dfil):
                continue

            opciones.append(dir)

        if len(opciones) == 0:
            return opuesta

        return random.choice(opciones)

    def calcular_objetivo(
        self, mapa, pacman
    ):  # default simple, a reemplazar en cada fantasma, menos en blinky
        """
        Calcula el objetivo del fantasma, que por defecto es la posición actual de Pacman. Este método se espera que sea reemplazado en cada clase de fantasma para implementar su comportamiento específico.
        Argumentos: mapa: el mapa del juego, utilizado para calcular la posición de Pacman.
                    pacman: el objeto Pacman, del cual se obtiene su posición actual para calcular el objetivo.
        Retorna: Una tupla (fila_objetivo, col_objetivo) que representa la posición objetivo a la que el fantasma se dirige, que por defecto es la posición actual de Pacman en términos de fila y columna en el mapa.
        """
        return self.tile_dexy(pacman.x, pacman.y, mapa)

    def calcular_inversa(self, mapa):
        """
        Calcula la dirección opuesta a la actual del fantasma y actualiza su destino en consecuencia. Este método se utiliza para cambiar la dirección del fantasma cuando está asustado o cuando muere, haciendo que se aleje de Pacman o regrese a la casa de los fantasmas.
        Argumentos: mapa: el mapa del juego, utilizado para calcular la nueva posición del fantasma después de cambiar su dirección.
        Retorna: None
        """
        if self.destino is None:
            return
        opuestas = {...}
        opuestas = {
            "arriba": "abajo",
            "abajo": "arriba",
            "izquierda": "derecha",
            "derecha": "izquierda",
        }
        self.direccion = opuestas[self.direccion]
        fila, columna, _ = self.direccion_vecina(
            mapa, self.destino[0], self.destino[1], self.direccion
        )
        self.destino = (fila, columna)

    def camino_a(self, mapa, inicio, objetivo):
        """
        Calcula la dirección a tomar para ir desde una posición de inicio hasta un objetivo utilizando una búsqueda en anchura (BFS) en el mapa, evitando paredes y teniendo en cuenta las restricciones de movimiento del fantasma. Este método se utiliza para que el fantasma pueda encontrar el camino hacia su objetivo, ya sea Pacman o la casa de los fantasmas, dependiendo de su estado actual.
        Argumentos: mapa: el mapa del juego, utilizado para verificar paredes y calcular posiciones.
                    inicio: una tupla (fila_inicio, col_inicio) que representa la posición de inicio desde la cual se quiere calcular el camino.
                    objetivo: una tupla (fila_objetivo, col_objetivo) que representa la posición objetivo a la cual se quiere llegar.
        Retorna: La dirección ("arriba", "abajo", "izquierda", "derecha") que el fantasma debe tomar para avanzar hacia el objetivo desde la posición de inicio, o None si no hay un camino válido.
        """
        cola = [inicio]
        vino_de = {inicio: None}
        while cola:
            actual = cola.pop(0)
            if actual == objetivo:
                break
            fila, col = actual
            for direccion in ["arriba", "abajo", "izquierda", "derecha"]:
                dfil, dcol, _ = self.direccion_vecina(mapa, fila, col, direccion)
                vecino = (dfil, dcol)
                if vecino in vino_de or self.es_pared(mapa, dcol, dfil):
                    continue
                vino_de[vecino] = (actual, direccion)
                cola.append(vecino)
        if inicio == objetivo:
            return self.direccion
        if objetivo not in vino_de:
            return self.direccion
        paso = objetivo
        primera = None
        while vino_de[paso] is not None:
            anterior, direccion = vino_de[paso]
            primera = direccion
            paso = anterior
        return primera

    def actualizar(self, dt, mapa, pacman, modo, puntos_comidos):
        """Actualiza el estado, movimiento y comportamiento del
        fantasma según su situación actual.

        Argumentos:
            dt(float): tiempo transcurrido desde el último frame.
            mapa: el mapa del juego.
            pacman: la instancia de Pacman.
            modo(str): el modo actual del juego.
            puntos_comidos(int): los puntos comidos por Pacman.

        Retorna:
            None.
        """
        self.actualizar_asustado(dt)

        if self.encerrado:
            if puntos_comidos >= self.umbral:
                self.encerrado = False
                self.saliendo_casa = True
            else:
                return

        if self.destino is None:
            self.destino = self.tile_actual(mapa)
        fila_a, col_a = self.tile_actual(mapa)
        centro_d = self.calcular_centro(self.destino[0], self.destino[1], mapa)
        pos_a = pygame.Vector2(self.x, self.y)
        paso = self.velocidad_actual(mapa) * dt
        if (
            pos_a.distance_to(centro_d) <= paso
        ):  # para evitar error acumulado al centrar
            self.x = centro_d.x
            self.y = centro_d.y
            fila_d = self.destino[0]
            col_d = self.destino[1]
            _, _, opuesta = self.direccion_vecina(
                mapa, fila_d, col_d, self.direccion
            )  # el _ porque no nos importa

            if self.muerto:
                objetivo = (14, 13)
                self.direccion = self.camino_a(mapa, (fila_d, col_d), objetivo)
                self.destino = self.direccion_vecina(
                    mapa, fila_d, col_d, self.direccion
                )[:2]
                if (fila_d, col_d) == objetivo:
                    self.muerto = False
                    self.saliendo_casa = True
                return
            if self.saliendo_casa:
                salida = (11, 13)
                self.direccion = self.camino_a(mapa, (fila_d, col_d), salida)
                self.destino = self.direccion_vecina(
                    mapa, fila_d, col_d, self.direccion
                )[:2]

                if (fila_d, col_d) == salida:
                    self.saliendo_casa = False

                return

            elif self.asustado:
                self.direccion = self.proxima_direccion_asustado(
                    mapa, opuesta, fila_d, col_d
                )
                self.destino = self.direccion_vecina(
                    mapa, fila_d, col_d, self.direccion
                )[:2]

            else:
                if modo == "SCATTER":
                    objetivo = self.esquina
                else:
                    objetivo = self.calcular_objetivo(mapa, pacman)

                self.direccion = self.proxima_direccion(
                    mapa, opuesta, fila_d, col_d, objetivo
                )
                self.destino = self.direccion_vecina(
                    mapa, fila_d, col_d, self.direccion
                )[:2]

        else:
            vector_direccion = (centro_d - pos_a).normalize()
            self.x = (pos_a + vector_direccion * paso).x
            self.y = (pos_a + vector_direccion * paso).y
        # caso tunel
        if self.x < mapa.offset_x:
            self.x += mapa.ancho
            self.destino = (self.destino[0], self.destino[1] + mapa.columnas)
        elif self.x > mapa.offset_x + mapa.ancho:
            self.x -= mapa.ancho
            self.destino = (self.destino[0], self.destino[1] - mapa.columnas)


# cada fantasma hereda los atributos de la clase Fantasma
class Blinky(Fantasma):
    pass


class Pinky(Fantasma):
    def calcular_objetivo(self, mapa, pacman):
        """
        Calcula el objetivo de Pinky ubicando un punto cuatro
        casillas por delante de la dirección actual de Pac-Man.

        Argumentos:
            mapa: mapa del juego.
            pacman: instancia de Pac-Man.

        Retorna:
            tuple[int, int]: fila y columna del objetivo de persecución.
        """

        fila, columna = self.tile_dexy(pacman.x, pacman.y, mapa)
        pacdeltafila, pacdeltacol = DELTAS[pacman.direccion]
        return (fila + pacdeltafila * 4, columna + pacdeltacol * 4)


class Inky(Fantasma):
    def __init__(self, x, y, nombre, color, puntaje, velocidad, compa):
        super().__init__(x, y, nombre, color, puntaje, velocidad)
        self.compa = compa

    def calcular_objetivo(self, mapa, pacman):
        """
        Calcula el objetivo de Inky tomando un punto dos casillas
        por delante de Pac-Man y reflejándolo respecto de la
        posición de su fantasma compañero.

        Argumentos:
            mapa: mapa del juego.
            pacman: instancia de Pac-Man.

        Retorna:
            tuple[int, int]: fila y columna del objetivo de persecución.
        """

        pacfila, paccol = self.tile_dexy(pacman.x, pacman.y, mapa)
        pacdeltafila, pacdeltacol = DELTAS[pacman.direccion]
        puntof = pacfila + pacdeltafila * 2
        puntocol = paccol + pacdeltacol * 2
        blinky_f, blinky_col = self.compa.tile_actual(mapa)
        return (2 * puntof - blinky_f, 2 * puntocol - blinky_col)


class Clyde(Fantasma):
    def calcular_objetivo(self, mapa, pacman):
        """
        Determina el objetivo de Clyde según su distancia a
        Pac-Man. Si está lejos lo persigue y si está cerca
        regresa a su esquina asignada.

        Argumentos:
            mapa: mapa del juego.
            pacman: instancia de Pac-Man.

        Retorna:
            tuple[int, int]: fila y columna del objetivo seleccionado.
        """

        pacfila, paccol = self.tile_dexy(pacman.x, pacman.y, mapa)
        ffila, fcol = self.tile_actual(mapa)
        dist = ((pacfila - ffila) ** 2 + (paccol - fcol) ** 2) ** 0.5
        if dist > 8:
            return (pacfila, paccol)
        else:
            return self.esquina


class Fantasma5(Fantasma):
    def calcular_objetivo(self, mapa, pacman):
        """
        Calcula un objetivo mostrando la posición de Pac-Man
        respecto al centro del mapa.

        Argumentos:
            mapa: mapa del juego.
            pacman: instancia de Pac-Man.

        Retorna:
            tuple[int, int]: fila y columna del objetivo reflejado.
        """
        pacman_fila, pacman_col = self.tile_dexy(pacman.x, pacman.y, mapa)
        centro_fila = mapa.filas // 2
        centro_col = mapa.columnas // 2
        # reflejo la posicion de pacman al lado opuesto del centro
        objetivo_fila = 2 * centro_fila - pacman_fila
        objetivo_col = 2 * centro_col - pacman_col
        return (objetivo_fila, objetivo_col)


class Fantasma6(Fantasma):
    def calcular_objetivo(self, mapa, pacman):
        """
        Calcula el objetivo de forma impredecible. Existe una
        probabilidad de elegir una posición aleatoria del mapa, y
        en caso contrario, persigue directamente a Pac-Man.

        Argumentos:
            mapa: mapa del juego.
            pacman: instancia de Pac-Man.

        Retorna:
            tuple[int, int]: fila y columna del objetivo seleccionado.
        """
        if random.random() < 0.25:
            return (
                random.randint(0, mapa.filas - 1),
                random.randint(0, mapa.columnas - 1),
            )
        return self.tile_dexy(pacman.x, pacman.y, mapa)
