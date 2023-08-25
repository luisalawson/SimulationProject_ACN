import pygame
import random
import matplotlib.pyplot as plt


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

    
    def eleccionVelocidad(self, congestion, tipoDeVehiculo):
        # si la congestion es alta, la velocidad va a estar 
        # concentrada en valores bajos
        # si la congestion es baja, la velocidad va a estar 
        # concentrada sobre valores mas cercanos a la velocidad maxima
        ...
    
    def tipoDeVehiculo(cls):
        
        #si es auto --> 60% de probabilidad
        #si es camion --> 10% de probabilidad
        #si es moto --> 30% de probabilidad
        
        probabilidades = [0.6, 0.1, 0.3]
        valores = ["auto", "camion", "moto"]
        return random.choices(valores, weights=probabilidades)[0]
    
    def dimensiones(cls, tipoDeVehiculo):
        
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
           

    def velocidad(self):
        ...

    def actualizar(self):
        #deberia tomar en cuenta la aceleracion + la velocidad + la posicion
        self.rect.x += self.speed


class Transito:
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Highway Simulation")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.autosEnTramo = []

    def diaSemana(n):
        dias = []
        for i in range(0,n):
            #elijo usar una uniforme porque la semana se distribuye asi
            # 1 -- Lunes, 2 -- Martes, 3 -- Miercoles, ... , 7 -- Domingo
            diaElegido = random.uniform(1, 7)
            dias.append(diaElegido)
        return dias
    
    def horaDelDia(self,n):
        horas = []
        for i in range(0,n):
            #elijo usar una uniforme porque el dia se distribuye asi
            # 0 -- 00:00, 1 -- 01:00, 2 -- 02:00, ... , 23 -- 23:00
            horaElegida = random.uniform(0, 23)
            horas.append(horaElegida)
        return horas
    
    def congestionHoraDia(self, hora, dia):
        #dado un dia y una hora, calcula la congestion que habra
        #esto me va a servir para saber cuantos autos mandar
        #en horarios donde hay mayor congestion, habran mas autos
        ...


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

