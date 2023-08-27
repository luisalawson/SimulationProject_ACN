import pygame
import random
import numpy as np
import time

random.seed(48279282)

pygame.init()

# 17 km
SCREEN_WIDTH = 1700
SCREEN_HEIGHT = 200

# Color del fondo
WHITE = (255, 255, 255)


#Creamos la clase Auto
class Auto(pygame.sprite.Sprite):
    
    #Atributos del auto
    def __init__(self, posicion, color, hora, dia):
        
        super().__init__()
        
        #Personalidad del conductor
        self.personalidadConductor_ = self.personalidadConductor()
        
        #Imagen del auto para la visualizacion y su color
        self.image = pygame.Surface((10, 20))
        self.image.fill(color)

        #Posicion inicial y velocidad dependiendo del dia y la hora
        self.dia = dia
        self.rect = self.image.get_rect()
        self.rect.x = posicion
        self.horaInicio = hora
        
        # Almacenamos la velocidad en km/minuto
        self.speed = self.eleccionVelocidad(hora,dia) / 60
        
        #Hora de llegada
        self.horaFin = None    

    #Calculamos velocidad dependiendo de la hora y el dia
    def eleccionVelocidad(self, hora, dia):
        
        # Inicializamos la velocidad en cero
        velocidadElegida = 0
        
        # Dia de semana + Congestion baja
        if ((0 <= hora < 6) or (22 <= hora < 24)) and dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']:
            velocidadElegida += np.random.normal(78.32, 1)
        
        # Dia de semana + Congestion moderada  
        elif ((6 <= hora < 7) or (20 <= hora < 22)) and dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']:
            velocidadElegida += np.random.normal(69.25, 2)
            
        # Dia de semana + Congestion critica
        elif ((7 <= hora < 8) or (11 <= hora < 20)) and dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']:
            velocidadElegida += np.random.normal(53.63, 6)
            
        # Dia de semana + Congestion pico
        elif (8 <= hora < 11) and dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']:
            velocidadElegida += np.random.normal(25.68, 5)
        
        # Sabado + Congestion baja
        elif ((0 <= hora < 7) or (23 <= hora < 24)) and dia == "Sabado":
            velocidadElegida += np.random.normal(78.46, 1)
            
        # Sabado + Congestion moderada
        elif ((7 <= hora < 10) or (22 <= hora < 23)) and dia == "Sabado":
            velocidadElegida += np.random.normal(71.64, 4)
            
        # Sabado + Congestion critica
        elif ((10 <= hora < 11) or (17 <= hora <= 22)) and dia == "Sabado":
            velocidadElegida += np.random.normal(59.58, 4)
        
        # Sabado + Congestion pico
        elif (11 <= hora < 17) and dia == "Sabado":
            velocidadElegida += np.random.normal(48.01, 3)
        
        # Domingo + Congestion baja
        elif ((0 <= hora < 11) or (22 <= hora < 24)) and dia == "Domingo":
            velocidadElegida += np.random.normal(78.46, 1)
            
        # Domingo + Congestion moderada
        elif ((11 <= hora < 12) or (15<=hora<16) or (20 <= hora < 22)) and dia == "Domingo":
            velocidadElegida += np.random.normal(70.43, 3)
            
        # Domingo + Congestion critica
        elif (16 <= hora < 20) and dia == "Domingo":
            velocidadElegida += np.random.normal(60.94, 2)
            
        # Domingo + Congestion pico
        elif (12 <= hora < 15) and dia == "Domingo":
            velocidadElegida += np.random.normal(53.97, 5)
    
        else:
            raise ValueError("Hora no válida")
    
    # Vemos como afecta la personalidad del conductor a la velocidad
        
        # Si el conducto es agresivo, la velocidad aumenta
        if self.personalidadConductor_ == "Agresivo":
            velocidadElegida += random.uniform(5, 10)
        
        # Si el conductor es moderado, la velocidad se mantiene
        elif self.personalidadConductor_ == "Moderado":
            velocidadElegida += random.uniform(0, 5)
            
        # Si el conductor es lento, la velocidad disminuye
        elif self.personalidadConductor_ == "Lento":
            velocidadElegida += random.uniform(-10, -5)
            
        else:
            raise ValueError("Tipo de conductor no válido")
        
        return velocidadElegida

    # Definimos la personalidad del conductor
    def personalidadConductor(self):
        
        # Definimos personalidades y sus probabilidades
        valores = ['Agresivo', 'Moderado', 'Lento']
        probabilidades = [0.2, 0.7, 0.1]
        
        # Elegimos una personalidad al azar
        personalidad = random.choices(valores, weights=probabilidades)[0]
        
        return personalidad
    
    # Actualizamos la posicion del auto a cada minuto
    def actualizar(self):
        
        # Actualizamos la posicion sumandole la velocidad (en km/minuto)
        self.rect.x += self.speed

        # Si el auto llega al final de la pantalla, guardamos la hora de llegada
        if self.rect.x >= SCREEN_WIDTH:
            self.horaFin = pygame.time.get_ticks()
            self.speed = 0

    # Calculamos el tiempo que tarda el auto en recorrer el tramo
    def tiempoRecorrido(self):
        
        if self.horaFin is not None:
            tiempoPasado = (self.horaFin - self.horaInicio) 
            return tiempoPasado
        
        else:
            return None


# Creamos la clase Autopista
class Autopista:
    
    # Definimos atributos del Autopista
    def __init__(self):
        
        # Definimos el dia de la semana y la hora del dia
        self.diaSemana_ = self.diaSemana()
        self.horaDelDia_ = self.horaDelDia()
        
        # Creamos variable para almacenar la cantidad de autos en el tramo
        # En una autopista de 17 km, la cantidad de autos va desde 0 a 3000
        # Cuando la cantidad de autos es baja, hay poco transito.
        # Cuando la cantidad de autos es alta, hay mucho transito.
        # Esto va a depender de el dia y la hora.
    
        self._cantidadAutos = self.cantidadAutos(self.diaSemana_, self.horaDelDia_)
        self._autosEnTramo = []

    # Definimos el dia de la semana
    def diaSemana(self):
        
        # Definimos los dias de la semana y sus probabilidades
        dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
        
        #Elegimos un dia al azar
        diaElegido = random.choices(dias)[0]
        
        return diaElegido

    # Definimos la hora del dia
    def horaDelDia(self):
        
        # Elegimos una hora al azar
        hora_seleccionada = random.uniform(0, 24)
        return hora_seleccionada
    
    # Dependiendo del dia y la hora, la autopista (nuestra muestra) tendra una cantidad de autos distinta
    def cantidadAutos(self, dia, hora):
        
        #Si es dia de semana
        if(dia == 'Lunes' or dia == 'Martes' or dia == 'Miercoles' or dia == 'Jueves' or dia == 'Viernes'):
            
            if(0 <= hora < 9 or 20 <= hora <= 24):
                cantidadAutos = random.randint(2000, 3000)
            elif(9 <= hora < 11):
                cantidadAutos = random.randint(1, 800)
            elif(11 <= hora < 20 ):
                cantidadAutos = random.randint(800, 2000)
            else:
                raise ValueError("Hora no válida")
        
        #Si es Sabado
        elif(dia == 'Sabado'):
            
            if(0 <= hora < 12 or 22 <= hora <= 23):
                cantidadAutos = random.randint(1, 800)
            elif(12 <= hora < 19):
                cantidadAutos = random.randint(2000, 3000)
            elif(19 <= hora < 22):
                cantidadAutos = random.randint(800, 2000)
            else:
                raise ValueError("Hora no válida")
            
        #Si es Domingo
        elif(dia == 'Domingo'):
            
            if(0 <= hora <= 11 or 21 <= hora <= 23):
                cantidadAutos = random.randint(1, 800)
            elif(12 <= hora <= 14):
                cantidadAutos = random.randint(2000, 3000)
            elif(15 <= hora <= 20):
                cantidadAutos = random.randint(800, 2000)
            else:
                raise ValueError("Hora no válida")
            
        else:
            raise ValueError("Dia no válido")
        
        
        return cantidadAutos


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Liniers - Lugones | Simulacion de Autopista")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

Autopista = Autopista()

print(f"Dia: {Autopista.diaSemana_}")
print(f"Hora: {Autopista.horaDelDia_}")
print(f"Cantidad de autos: {Autopista._cantidadAutos}")

for _ in range(Autopista._cantidadAutos):
    
    posicion = 0
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    hora = Autopista.horaDelDia_
    dia = Autopista.diaSemana_
    
    auto = Auto(posicion, color, hora, dia)
    
    Autopista._autosEnTramo.append(auto)
    
    all_sprites.add(auto)

running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)


    for i in range(0, len(Autopista._autosEnTramo)):
        
        #Si el auto es el primero -> que avance
        if (i == 0):
            auto.actualizar()

        #Si el auto no es el primero
        else:
            
            #Si el auto ya termino de recorrer el tramo -> que no avance
            if (Autopista._autosEnTramo[i].rect.x >= SCREEN_WIDTH):
                continue
                
            #Si el auto de adelante esta a menor distancia de la velocidad de mi auto, no lo actualizo
            elif(Autopista._autosEnTramo[i-1].rect.x - Autopista._autosEnTramo[i].rect.x < Autopista._autosEnTramo[i].speed):
                auto.actualizar()
        
    #Checkeo si TODOS los autos terminaron de recorrer el tramo, termino la simulacion
    value = True
    
    for k in range(0, len(Autopista._autosEnTramo)):
        if (Autopista._autosEnTramo[k].horaFin is None):
            value = False
        else:
            continue
                
    if (value):
        running = False
        
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

for auto in Autopista._autosEnTramo:
    tiempo = auto.tiempoRecorrido()
    if tiempo is not None:
        tiempo = tiempo/60
        print(f"Auto {auto.horaInicio:.2f}: Tiempo recorrido: {tiempo:.2f} minutos")