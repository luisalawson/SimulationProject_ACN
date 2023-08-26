import pygame
import random
import matplotlib.pyplot as plt
import numpy as np

random.seed(48279282)

pygame.init()

# 17 km
SCREEN_WIDTH = 1700
SCREEN_HEIGHT = 200

# Color del fondo
WHITE = (255, 255, 255)

# Genero la clase auto
class Auto(pygame.sprite.Sprite):
    
    def __init__(self, posicion, color):
        
        super().__init__()
        
        self.tipoDeVehiculo_ = self.tipoDeVehiculo()
        self.personalidadConductor_ = self.personalidadConductor()
        
        #la imagen del auto para la vis
        self.dimensiones = self.dimensiones(self.tipoDeVehiculo_)
        
        self.image = pygame.Surface(self.dimensiones)
        self.image.fill(color)

        self.rect = self.image.get_rect()
        
        #la posicion inicial y la velocidad
        self.rect.x = posicion
        self.speed = velocidad
    
    def eleccionVelocidad(self, tipoDeConductor, hora):
        # si la congestion es alta, la velocidad va a estar 
        # concentrada en valores bajos
        # si la congestion es baja, la velocidad va a estar 
        # concentrada sobre valores mas cercanos a la velocidad maxima
        velocidadElegida=0
        if hora == "Baja":
            velocidadElegida += np.random.normal(78.26,1)
        elif hora == "Moderada":
            velocidadElegida += np.random.normal(69.06,2)
        elif hora == "Critica":
            velocidadElegida += np.random.normal(54.97,5)
        elif hora == "Pico":
            velocidadElegida += np.random.normal(39.30,3)
        else:
            raise ValueError("Hora no válida")
        
        if tipoDeConductor == "Agresivo":
            velocidadElegida += random.uniform(5,10)
        elif tipoDeConductor == "Moderado":
            velocidadElegida += random.uniform(-2,5)
        elif tipoDeConductor == "Lento":
            velocidadElegida += random.uniform(-10,-5)
        else:
            raise ValueError("Tipo de conductor no válido")
        return velocidadElegida
    
    def tipoDeVehiculo(self):
        
        #si es auto --> 60% de probabilidad
        #si es camion --> 10% de probabilidad
        #si es moto --> 30% de probabilidad
        
        probabilidades = [0.6, 0.1, 0.3]
        valores = ["auto", "camion", "moto"]
        return random.choices(valores, weights=probabilidades)[0]
    
    def dimensiones(self, tipoDeVehiculo):
        
        if tipoDeVehiculo == "auto":
            return (40, 20)
        elif tipoDeVehiculo == "camion":
            return (40, 30)
        elif tipoDeVehiculo == "moto":
            return (40, 10)
        else:
            raise ValueError("Tipo de vehiculo no valido")
    
    
    
    def personalidadConductor(self):
        #si es agresivo --> la velocidad elegida siempre es la maxima o mas
        #               --> deja poco espacio con el de adelante
        # si es moderado --> la velocidad elegida siempre es un poco debajo de la maxima
        #               --> deja moderado espacio con el de adelante
        # si es lento --> la velocidad elegida siempre es un por debajo de la maxima
        #               --> deja mucho espacio con el de adelante

        probabilidades = [0.2, 0.7, 0.1]
        valores = ['agresivo','moderado','lento']
        self.personalidadConductor_ = random.choices(valores,weights=probabilidades)
           

    def actualizar(self):
        #deberia tomar en cuenta la aceleracion + la velocidad + la posicion
        self.rect.x += self.speed


class Transito:
    
    def _init_(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Highway Simulation")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.diaSemana_ = self.diaSemana()
        self.horaDelDia_ = self.horaDelDia()
        self.autosEnTramo = []

    def diaSemana(self):
        dias = ['Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo']
        probabilidades = [0.14,0.15,0.16,0.16,0.15,0.13,0.11]
        diaElegido = random.choices(dias, weights=probabilidades)[0]
        return diaElegido
    
    def horaDelDia(self):
        horas = random.randint(0,24)
        if self.diaSemana_=="Lunes" or self.diaSemana_=="Martes" or self.diaSemana_=="Miercoles"or self.diaSemana_=="Jueves" or self.diaSemana_=="Viernes":
            muestrasUno = np.random.normal(9,3,10000)
            muestrasDos = np.random.normal(18,4,10000)
            muestrasHoras = np.concatenate((muestrasUno,muestrasDos))
            horaElegida = random.choices(muestrasHoras)
        elif self.diaSemana_=="Sabado":
            muestrasUno = np.random.normal(13,3, 10000)
            muestrasDos = np.random.normal(20,1,10000)
            muestrasHoras = np.concatenate((muestrasUno,muestrasDos))
            horaElegida = random.choices(muestrasHoras)
        elif self.diaSemana_=="Domingo":
            muestrasUno = np.random.normal(13,2,10000)
            muestrasDos = np.random.normal(18,3,10000)
            muestrasHoras = np.concatenate((muestrasUno,muestrasDos))
            horaElegida = random.choices(muestrasHoras)
        else:
            raise ValueError("Día no válido")
        return horaElegida
    
   
    def congestionHoraDia(self, hora, dia):
        #dado un dia y una hora, calcula la congestion que habra
        #esto me va a servir para saber cuantos autos mandar
        #en horarios donde hay mayor congestion, habran mas autos
        return
    
# Pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Highway Simulation")
clock = pygame.time.Clock()

# Pygame sprite group
all_sprites = pygame.sprite.Group()


n = 20  # cantidad de autos generados en el primer instante
autos = []
for _ in range(n):
    velocidad = random.randint(1, 5) # velocidad random -- CAMBIAR A DISTRIBUCION
    posicion = 0  # los autos entran desde la ubicacion inicial, entonces es 0 siempre
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # color random para diferenciar los autos
    auto = Auto(posicion, color) # ahora con eso creo mi auto
    autos.append(auto) # inserto el auto en el plano que cree
    all_sprites.add(auto) # lo agrego a mi visualizacion

# loop para la visualizacion
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # # voy actualizando los autos para que no hayan choques -- HACER
    for i in range(len(autos)):
        auto_i = autos[i]
        auto_i.actualizar()

        # if i > 0:
        #     # chequeo la distancia del auto de adelante
        #     distancia = autos[i - 1].rect.left - auto.rect.right

        #     if distancia < 5:  # si la distancia es menor a 5 bajo la velocidad para evitar choque
        #         auto.speed += 10 #le resto la velocidad para que no se choque

    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second

pygame.quit()


