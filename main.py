import math
import random

class Planet:
    def __init__(self, pos, r, v, m, color, name=None):
        self.name = name
        if name == None:
            self.name = f"Planet {len(planets) + 1}"
        self.pos = pos
        self.r = r
        self.v = v
        self.m = m
        self.color = color

    def update(self):
        a = [0, 0]
        for p in planets:
            if p != self:
                
                dx = (self.pos[0] - p.pos[0])*1000*1000
                dy = (self.pos[1] - p.pos[1])*1000*1000

                if dx != 0 or dy != 0:
                    acc = G*p.m/(dx**2 + dy**2)
                if dx != 0:
                    alfa = math.atan(abs(dy/dx))
                else:
                    alfa = math.pi/2

                if p.pos[0] > self.pos[0]:
                    a[0] += acc*math.cos(alfa)
                else:
                    a[0] -= acc*math.cos(alfa)
                if p.pos[1] > self.pos[1]:
                    a[1] += acc*math.sin(alfa)
                else:
                    a[1] -= acc*math.sin(alfa)

            # print(p.name, (dx**2 + dy**2)**(1/2), (self.v[0]**2 + self.v[1]**2)**(1/2))

        self.v[0] += a[0]/1000/1000*10
        self.v[1] += a[1]/1000/1000*10

        self.pos[0] += self.v[0]/FPS
        self.pos[1] += self.v[1]/FPS


    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, self.r)

planets = []
sun = Planet([400, 300], 700/2/10, [0, 0], 1.989*10**30, (255, 255, 0), "Sun")
planets.append(sun)
mercury = Planet([330.2, 300], 2.4/2, [0, 38.86], 3.301*10**23, (128, 128, 128, "Mercury"))
planets.append(mercury)
venus = Planet([292, 300], 6.6/2, [0, 35], 4.8675*10**24, (255, 128, 0), "Venus")
planets.append(venus)
earth = Planet([247.9, 300], 6.3/2, [0, 29.3], 5.972*10**24, (0, 0, 255), "Earth")
planets.append(earth)
mars = Planet([172, 300], 3.5/2, [0, 21.972], 6.4185*10**23, (255, 0, 0), "Mars")
planets.append(mars)

import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Gravity Engine")

FPS = 100
clock = pygame.time.Clock()

G = 6.67408*10**-11

while True:
    screen.fill((0, 0, 0))
    for p in planets:
        p.update()
        p.draw()

    to_remove = []
    to_add = []

    for planet in planets:
        for p in planets:
            if p != planet:
                if (p.pos[0]-planet.pos[0])**2 + (p.pos[1]-planet.pos[1])**2 < (p.r + planet.r)**2:
                    
                    if planet.r > p.r:
                        pos = planet.pos
                    else:
                        pos = p.pos

                    r = (p.r**3 + planet.r**3)**(1/3)

                    m = p.m+planet.m

                    v_x = (p.m*p.v[0] + planet.m*planet.v[0])/m
                    v_y = (p.m*p.v[1] + planet.m*planet.v[1])/m
                    v = [v_x, v_y]

                    print(p.color, planet.color)
                    red = int((p.color[0]*p.m + planet.color[0]*planet.m)/m)
                    blue = int((p.color[1]*p.m + planet.color[1]*planet.m)/m)
                    green = int((p.color[2]*p.m + planet.color[2]*planet.m)/m)
                    color = (red, green, blue)
                    print(color)

                    planets.append(Planet(pos, r, v, m, color))
                    planets.remove(p)
                    planets.remove(planet)
                    break
        else:
            continue
        break

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            planets.append(Planet(list(mouse), 6, [0, 0], 2*10**24, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

    pygame.display.update()