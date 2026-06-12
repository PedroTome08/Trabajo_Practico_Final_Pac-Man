import pygame

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
    def calcular_centro(self,fila,col,mapa):
        x=mapa.offset_x +col *mapa.tile +mapa.tile/2
        y= mapa.offset_y +fila *mapa.tile +mapa.tile/2   
        return pygame.Vector2(x, y)
    def vecina(self,mapa, fila,col,direccion):
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
    def proxima_direccion(self,mapa,opuesta,fila,col):
        posibles = []
        for i in ["arriba","abajo","izquierda","derecha"]:
            df, dc, falsa_o = self.vecina(mapa,fila,col,i)
            if i == opuesta: continue
            elif not self.es_pared(mapa,dc,df):
                posibles.append(i)
        if self.direccion in posibles:
            return self.direccion
        if posibles:    
            return posibles[0]
        else: return opuesta   
                
    def actualizar(self, dt, mapa):
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
            _,_, opuesta= self.vecina(mapa,fila_d,col_d,self.direccion) # el _ porque no nos importa
            self.direccion = self.proxima_direccion(mapa,opuesta,fila_d,col_d)   
            self.destino = self.vecina(mapa,fila_d,col_d,self.direccion)
        else:
            vector_direccion = (centro_d-pos_a).normalize()
            self.x = (pos_a + vector_direccion * paso).x 
            self.y = (pos_a + vector_direccion * paso).y
#cada fantasma hereda los atributos de la clase Fantasma
class Blinky(Fantasma):
    pass

class Pinky(Fantasma):
    pass

class Inky(Fantasma):
    pass

class Clyde(Fantasma):
    pass

class Fantasma5(Fantasma):
    pass

class Fantasma6(Fantasma):
    pass