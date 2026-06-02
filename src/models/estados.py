class Estado:
    def __init__(self):
        self.fase = [("SCATTER", 7), ("CHASE", 20), ("SCATTER", 7), ("CHASE", 20), ("SCATTER", 5), ("CHASE", 20), ("SCATTER", 5), ("CHASE", None)] #cada fase con el tiempo que dura cada una
        
        self.fase_actual = 0
        self.modo_actual = "SCATTER"
        self.tiempo_fase = 0
        
    def actualizar(self, dt):
        self.tiempo_fase += dt
        
        duracion = self.fase[self.fase_actual][1]
        if duracion is not None and self.tiempo_fase >= duracion:
            self.fase_actual += 1 #sumo 1 para que pase a la siguiente fase
            self.tiempo_fase = 0 #reseteo el tiempo a 0 cuando empieza la proxima fase
            
            self.modo_actual = self.fase[self.fase_actual][0]
            
            return True #devuelve True si entro al if porque hubo cambio de fase
        
        return False #si no entra al if devuelve False porque no hubo cambio de fase
        
    def obtener_fase(self): #para que los fantasmas hagan fase = estado.obtener_fase()
        return self.modo_actual
    
    