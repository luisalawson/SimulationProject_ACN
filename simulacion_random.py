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

class Auto(pygame.sprite.Sprite):
    def __init__(self, posicion, color, hora, dia):
        super().__init__()
        self.personalidadConductor_ = self.personalidadConductor()
        self.image = pygame.Surface((40, 20))
        self.image.fill(color)

        self.dia = dia

        self.rect = self.image.get_rect()
        self.rect.x = posicion
        self.horaInicio = hora
        self.speed = self.eleccionVelocidad(hora,dia)
        self.horaFin = None    

    def eleccionVelocidad(self, hora, dia):
        velocidadElegida = 0
        if ((0 <= hora < 6) or (22 <= hora < 24)) and dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']:
            velocidadElegida += np.random.normal(78.32/(60), 1)
        elif ((6 <= hora < 7) or (20 <= hora < 22)) and dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']:
            velocidadElegida += np.random.normal(69.25/(60), 2)
        elif ((7 <= hora < 8) or (11 <= hora < 20)) and dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']:
            velocidadElegida += np.random.normal(53.63/(60), 6)
        elif (8 <= hora < 11) and dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']:
            velocidadElegida += np.random.normal(25.68/(60), 5)
        
        elif ((0 <= hora < 7) or (23 <= hora < 24)) and dia == "Sabado":
            velocidadElegida += np.random.normal(78.46/(60), 1)
        elif ((7 <= hora < 10) or (22 <= hora < 23)) and dia == "Sabado":
            velocidadElegida += np.random.normal(71.64/(60), 4)
        elif ((10 <= hora < 11) or (17 <= hora <= 22)) and dia == "Sabado":
            velocidadElegida += np.random.normal(59.58/(60), 4)
        elif (11 <= hora < 17) and dia == "Sabado":
            velocidadElegida += np.random.normal(48.01/(60), 3)
        
        elif ((0 <= hora < 11) or (22 <= hora < 24)) and dia == "Domingo":
            velocidadElegida += np.random.normal(78.46/(60), 1)
        elif ((11 <= hora < 12) or (15<=hora<16) or (20 <= hora < 22)) and dia == "Domingo":
            velocidadElegida += np.random.normal(70.43/(60), 3)
        elif (16 <= hora < 20) and dia == "Domingo":
            velocidadElegida += np.random.normal(60.94/(60), 2)
        elif (12 <= hora < 15) and dia == "Domingo":
            velocidadElegida += np.random.normal(53.97/(60), 5)
        

        else:
            raise ValueError("Hora no válida")
        
        if self.personalidadConductor_ == "Agresivo":
            velocidadElegida += random.uniform(5/60, 10/60)
        elif self.personalidadConductor_ == "Moderado":
            velocidadElegida += random.uniform(-2/60, 5/60)
        elif self.personalidadConductor_ == "Lento":
            velocidadElegida += random.uniform(-10/60, -5/60)
        else:
            raise ValueError("Tipo de conductor no válido")
        return velocidadElegida

    def personalidadConductor(self):
        probabilidades = [0.2, 0.7, 0.1]
        valores = ['Agresivo', 'Moderado', 'Lento']
        personalidad = random.choices(valores, weights=probabilidades)[0]
        return personalidad

    def actualizar(self):
        self.rect.x += self.speed

        if self.rect.x > SCREEN_WIDTH:
            self.horaFin = pygame.time.get_ticks()
            self.speed = 0

    def tiempoRecorrido(self):
        if self.horaFin is not None:
            tiempoPasado = (self.horaFin - self.horaInicio) 
            return tiempoPasado
        else:
            return None

class Transito:
    def __init__(self):
        self.diaSemana_ = self.diaSemana()
        self.horaDelDia_ = self.horaDelDia()
        self.autosEnTramo = []

    def diaSemana(self):
        dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
        probabilidades = [0.14, 0.15, 0.16, 0.16, 0.15, 0.13, 0.11]
        diaElegido = random.choices(dias, weights=probabilidades)[0]
        return diaElegido

    def horaDelDia(self):
        if self.diaSemana_ in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']:
            muestrasUno = np.random.normal(9, 3, 10000)
            muestrasDos = np.random.normal(18, 4, 10000)
            muestrasHoras = np.concatenate((muestrasUno, muestrasDos))
            horaElegida = random.choice(muestrasHoras)
        elif self.diaSemana_ == 'Sabado':
            muestrasUno = np.random.normal(13, 3, 10000)
            muestrasDos = np.random.normal(20, 1, 10000)
            muestrasHoras = np.concatenate((muestrasUno, muestrasDos))
            horaElegida = random.choice(muestrasHoras)
        elif self.diaSemana_ == 'Domingo':
            muestrasUno = np.random.normal(13, 2, 10000)
            muestrasDos = np.random.normal(18, 3, 10000)
            muestrasHoras = np.concatenate((muestrasUno, muestrasDos))
            horaElegida = random.choice(muestrasHoras)
        else:
            raise ValueError("Día no válido")
        return horaElegida


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Liniers - Lugones | Simulacion de transito")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

n = 5
autos = []
for _ in range(n):
    posicion = 0
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    transito = Transito()
    hora = transito.horaDelDia_
    dia = transito.diaSemana_
    auto = Auto(posicion, color, hora, dia)
    autos.append(auto)
    all_sprites.add(auto)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    for auto in autos:
        auto.actualizar()

    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

for auto in autos:
    tiempo = auto.tiempoRecorrido()
    if tiempo is not None:
        tiempo = tiempo/60
        print(f"Auto {auto.horaInicio:.2f}: Tiempo recorrido: {tiempo:.2f} minutos")