import pygame
DELTAS = {"arriba": (-1, 0), "abajo": (1, 0), "izquierda": (0, -1), "derecha": (0, 1)}

class Fantasma:
    def __init__(self, x, y, nombre, color, puntaje, velocidad):
        self.x = x
        self.y = y
        self.nombre = nombre
        self.color = color
        self.puntaje = puntaje
        self.velocidad = velocidad

        self.img_der = pygame.image.load(f"assets/images/{nombre.lower()}_der.png").convert_alpha() #metodo de pygame para cargar imagenes de los fantasmas
        self.img_izq = pygame.image.load(f"assets/images/{nombre.lower()}_izq.png").convert_alpha()

        self.img_der = pygame.transform.scale(self.img_der, (38, 38)) #metodo de pygame para ajustar el tamaño de la imagen de los fantasmas
        self.img_izq = pygame.transform.scale(self.img_izq, (38, 38))
        
        self.direccion = "izquierda"
        self.destino = None

        self.esquina = (-2,1) #placeholder, cambiar
    def es_pared(self,mapa,col,fila):
        if 0 <= fila < mapa.filas and 0 <= col < mapa.columnas:
            return mapa.grilla[fila][col] == "X"
        return True
    def dibujar_fantasmas(self, pantalla):
        if self.direccion == "derecha":
            pantalla.blit(self.img_der, (self.x- 19, self.y- 19)) #-19 por el sprite de 38x38 (/2=19) para que quede centrado
        else:
            pantalla.blit(self.img_izq, (self.x- 19, self.y- 19))
    def tile_actual(self,mapa):
        fila=int((self.y-mapa.offset_y)//mapa.tile) #redondear para abajo y calcular la columna y filas en la grilla (no en pixeles)
        col=int((self.x-mapa.offset_x)//mapa.tile) 
        return fila,col
    def tile_dexy(self,x,y,mapa):
        fila=int((y-mapa.offset_y)// mapa.tile)
        col=int((x-mapa.offset_x) //mapa.tile)
        return fila, col
    def calcular_centro(self,fila,col,mapa):
        x=mapa.offset_x +col *mapa.tile +mapa.tile/2
        y= mapa.offset_y +fila *mapa.tile +mapa.tile/2   
        return pygame.Vector2(x, y)
    def direccion_vecina(self,mapa, fila,col,direccion):
        if direccion == "arriba": 
            destino_fila = fila-1
            destino_col = col
            opuesta = "abajo"
        elif direccion == "abajo":
            destino_fila = fila+1
            destino_col = col
            opuesta = "arriba"
        elif direccion == "derecha":
            destino_fila = fila
            destino_col = col+1
            opuesta = "izquierda"
        elif direccion == "izquierda":
            destino_fila = fila
            destino_col = col-1
            opuesta = "derecha"
        return destino_fila,destino_col,opuesta
    def proxima_direccion(self,mapa,opuesta,fila,col, objetivo): #para cuando llega al objetivo
        mejor_dist_dir = [None,None]
        for dir in ["arriba","izquierda","abajo","derecha"]:
            if dir == opuesta: continue
            dfil,dcol,_=self.direccion_vecina(mapa,fila,col,dir)
            if self.es_pared(mapa,dcol,dfil): continue
            dist=((objetivo[0]-dfil)**2+(objetivo[1]-dcol)**2)**0.5
            if mejor_dist_dir[0] is None or dist<mejor_dist_dir[0]: 
                mejor_dist_dir[0]=dist
                mejor_dist_dir[1]=dir
        if mejor_dist_dir[0] == None: return opuesta
        else: return mejor_dist_dir[1]
    def calcular_objetivo(self, mapa, pacman): #default simple, a reemplazar en cada fantasma, menos en blinky
        return (self.tile_dexy(pacman.x,pacman.y,mapa)) 
    def actualizar(self, dt, mapa,pacman):
        if self.destino is None:
            self.destino = self.tile_actual(mapa)
        fila_a, col_a = self.tile_actual(mapa)
        centro_d = self.calcular_centro(self.destino[0],self.destino[1],mapa)
        pos_a = pygame.Vector2(self.x,self.y)
        paso = self.velocidad*dt
        if pos_a.distance_to(centro_d) <= paso: #para evitar error acumulado al centrar 
            self.x = centro_d.x
            self.y = centro_d.y  
            fila_d = self.destino[0]
            col_d = self.destino[1]
            _,_, opuesta= self.direccion_vecina(mapa,fila_d,col_d,self.direccion) # el _ porque no nos importa
            objetivo = self.calcular_objetivo(mapa,pacman)
            self.direccion = self.proxima_direccion(mapa,opuesta,fila_d,col_d,objetivo)   
            self.destino = self.direccion_vecina(mapa,fila_d,col_d,self.direccion)
        else:
            vector_direccion = (centro_d-pos_a).normalize()
            self.x = (pos_a + vector_direccion * paso).x 
            self.y = (pos_a + vector_direccion * paso).y
#cada fantasma hereda los atributos de la clase Fantasma
class Blinky(Fantasma):
    pass

class Pinky(Fantasma):
    def calcular_objetivo(self, mapa, pacman):
        fila,columna = self.tile_dexy(pacman.x,pacman.y,mapa)
        pacdeltafila, pacdeltacol = DELTAS[pacman.direccion]
        return (fila + pacdeltafila*4, columna + pacdeltacol*4)

class Inky(Fantasma):
    pass

class Clyde(Fantasma):
    def calcular_objetivo(self,mapa,pacman):
        pacfila,paccol = self.tile_dexy(pacman.x,pacman.y,mapa)
        ffila, fcol = self.tile_actual(mapa)
        dist = ((pacfila-ffila)**2+ (paccol-fcol)**2)**0.5
        if dist >8:
            return(pacfila,paccol)
        else: return self.esquina
class Fantasma5(Fantasma):
    pass

class Fantasma6(Fantasma):
    pass