import math
import random

class Planet:
    def __init__(self, pos, r, v, m, color, name = "Planet"):
        self.name = name
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

        self.v[0] += a[0]/1000/1000*10
        self.v[1] += a[1]/1000/1000*10

        self.pos[0] += self.v[0]/FPS
        self.pos[1] += self.v[1]/FPS

    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, self.r)
    
    def write(self, i):
        self.vel = (self.v[0]**2 + self.v[1]**2) ** (1/2)

        text_render = font.render(f"{self.name} : {round(self.vel, 2)} km/s (x: {round(self.v[0], 2)}, y: {round(self.v[1], 2)})", True, self.color)
        text_rect = text_render.get_rect(topleft = (WIDTH + 10, 10 + i*30))
        screen.blit(text_render, text_rect)

import pygame
from PIL import Image

pygame.init()

width_data_rect = 300
WIDTH = int(pygame.display.Info().current_w * 5/6) - width_data_rect
HEIGHT = int(pygame.display.Info().current_h * 5/6)

center_w = WIDTH/2
center_h = HEIGHT/2

planets = []
sun = Planet([center_w, center_h], 700/2/10, [0, 0], 1.989*10**30, (255, 255, 0), "Sun")
mercury = Planet([center_w - 69.8, center_h], 2.4/2, [0, 38.86], 3.301*10**23, (128, 128, 128), "Mercury")
venus = Planet([center_w - 108, center_h], 6.6/2, [0, 35], 4.8675*10**24, (255, 128, 0), "Venus")
earth = Planet([center_w - 152.1, center_h], 6.3/2, [0, 29.3], 5.972*10**24, (0, 0, 255), "Earth")
mars = Planet([center_w - 228, center_h], 3.5/2, [0, 21.972], 6.4185*10**23, (255, 0, 0), "Mars")
planets = [sun, mercury, venus, earth, mars]

screen = pygame.display.set_mode((WIDTH + width_data_rect, HEIGHT)) 
pygame.display.set_caption("Gravity Engine")

FPS = 100
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)

G = 6.67408*10**-11

number_keys = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

color_hue = pygame.image.load("color_hue.png")
color_hue_pixels = list(Image.open("color_hue.png").getdata())

game = True

while game:
    screen.fill((0, 0, 100))

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

                    v_x = (p.m*p.v[0] + planet.m * planet.v[0])/m
                    v_y = (p.m*p.v[1] + planet.m * planet.v[1])/m
                    v = [v_x, v_y]

                    red = int((p.color[0]*p.m + planet.color[0]*planet.m)/m)
                    green = int((p.color[1]*p.m + planet.color[1]*planet.m)/m)
                    blue = int((p.color[2]*p.m + planet.color[2]*planet.m)/m)
                    color = (red, green, blue)

                    planets.append(Planet(pos, r, v, m, color))
                    planets.remove(p)
                    planets.remove(planet)
                    break
        else:
            continue
        break

    for i in range(len(planets)):
        planets[i].update()
        planets[i].draw()

    pygame.draw.rect(screen, (0, 0, 0), (WIDTH, 0, width_data_rect, HEIGHT))
    pygame.draw.line(screen, (255, 255, 255), (WIDTH, 0), (WIDTH, HEIGHT))

    for i in range(len(planets)):
        planets[i].write(i)

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pos()[0] < WIDTH:
            planet = planet_w, planet_h = pygame.mouse.get_pos()
            
            rect_w, rect_h = 100, 20

            mass = "1*10**30"
            color = (255, 255, 255)

            done = False
            esc = False
            confirm = False

            while not confirm:
                mouse = mouse_x, mouse_y = pygame.mouse.get_pos()

                if not done:
                    screen.fill((0,0,100))

                    for i in range(len(planets)):
                        planets[i].draw()

                    try:
                        m = eval(mass) # instead of eval(), I could use the solve() function from my calculator app
                    except:
                        pass

                    if m < 10**24:
                        radius = 1
                    elif m < 10**25:
                        radius = 3
                    elif m < 10**27:
                        radius = 5
                    elif m < 10**30:
                        radius = 10
                    else:
                        radius = math.log(m, 10)

                    vel = [mouse_x-planet_w, mouse_y-planet_h]

                    pygame.draw.line(screen, (255, 0, 0), planet, mouse, 3)
                    dx = mouse_x-planet_w
                    dy = planet_h-mouse_y
                    k = 1
                    r = 10
                    if dx != 0 and dy != 0:
                        # x = 1/(2*(dx**2/dy**2+1)) * (-math.sqrt( ((2*dx*k)/dy-(2*dx*mouse_y)/dy-2*mouse_x)**2 - 4* (dx**2/dy**2+1) * (k**2-2*k*mouse_y+mouse_x**2+mouse_y**2-r**2) - (2*dx*k)/dy + (2*dx*mouse_y)/dy + 2*mouse_x))
                        x = planet_w + dx*0.95
                        y = planet_h - dy*0.95
                        x1 = x+dy*0.03
                        y1 = y+dx*0.03
                        x2 = x-dy*0.03
                        y2 = y-dx*0.03
                        pygame.draw.polygon(screen, (255, 0, 0), [mouse, (x1, y1), (x2, y2)])

                    p = Planet([planet_w, planet_h], radius, vel, 10**30, color)
                    p.draw()

                    pygame.draw.rect(screen, (0, 0, 0), (WIDTH, 0, width_data_rect, HEIGHT))
                    pygame.draw.line(screen, (255, 255, 255), (WIDTH, 0), (WIDTH, HEIGHT))

                    for i in range(len(planets)):
                        planets[i].write(i)
                    
                    p.write(i+1)

                    if (planet_w < WIDTH - 5 - rect_w + radius) and (planet_h > rect_h + 5 + radius):
                        rect = (planet_w - radius, planet_h - rect_h - radius - 5, rect_w, rect_h)
                        mass_render = font.render(mass, True, (0, 0, 0))
                        mass_rect = mass_render.get_rect(center = (planet_w - radius + rect_w/2, planet_h - rect_h - radius - 5 + rect_h/2))

                    elif (planet_h > rect_h + 5 + radius): # too far right
                        rect = (min(planet_w - rect_w + radius, WIDTH - 5 - rect_w), planet_h - rect_h - radius - 5, rect_w, rect_h)
                        mass_render = font.render(mass, True, (0, 0, 0))
                        mass_rect = mass_render.get_rect(center = (min(planet_w - rect_w + radius, WIDTH - 5 - rect_w) + rect_w/2, planet_h - rect_h - radius - 5 + rect_h/2))
                    
                    else: # top-right corner
                        rect = (min(planet_w - rect_w + radius, WIDTH - 5 - rect_w), planet_h + radius + 5, rect_w, rect_h)
                        mass_render = font.render(mass, True, (0, 0, 0))
                        mass_rect = mass_render.get_rect(center = (min(planet_w - rect_w + radius, WIDTH - 5 - rect_w) + rect_w/2, planet_h + radius + 5 + rect_h/2))
                    
                    pygame.draw.rect(screen, (255, 255, 255), rect, border_radius = 5)
                    screen.blit(mass_render, mass_rect)

                else:
                    point = (10, 10)
                    width = 10
                    pygame.draw.rect(screen, (0, 0, 0), (*point, 255 + 2 * width, 255 + 2 * width), border_radius = 5)
                    screen.blit(color_hue, (*(p + width for p in point), 255, 255)) # just a bit of fun with notation

                    if (point[0] + width < mouse_x < point[0] + width + 255) and (point[1] + width < mouse_y < point[1] + width + 255):
                        pixel_x = mouse_x - width - point[0]
                        pixel_y = mouse_y - width - point[1]
                        color = color_hue_pixels[pixel_y * 255 + pixel_x]
                        pygame.draw.circle(screen, color, mouse, 10)
                        pygame.draw.circle(screen, (0, 0, 0), mouse, 10, 1)

                        p = Planet([planet_w, planet_h], radius, vel, 10**30, color)
                        p.draw()

                        pygame.draw.rect(screen, (255, 255, 255), rect, border_radius = 5)
                        screen.blit(mass_render, mass_rect)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if not done:
                            if eval(mass) < 10**35:
                                done = True
                            else:
                                mass = "1*10**30"
                        else:
                            confirm = True

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            confirm = True
                            esc = True
                        elif event.key == pygame.K_BACKSPACE:
                            mass = mass[:-1]
                        elif event.key in number_keys:
                            mass += pygame.key.name(event.key)
                        elif event.key == pygame.K_DOLLAR and (pygame.KMOD_LSHIFT or pygame.KMOD_RSHIFT) and mass[-2:] != "**" and len(mass) > 0:
                            mass += "*"
                        elif event.key == pygame.K_SEMICOLON and (pygame.KMOD_LSHIFT or pygame.KMOD_RSHIFT):
                            mass += "."

                pygame.display.update()

            if not esc:
                planets.append(Planet(list(planet), radius, vel, m, color)) 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                sun = Planet([center_w, center_h], 700/2/10, [0, 0], 1.989*10**30, (255, 255, 0), "Sun")
                mercury = Planet([center_w - 69.8, center_h], 2.4/2, [0, 38.86], 3.301*10**23, (128, 128, 128), "Mercury")
                venus = Planet([center_w - 108, center_h], 6.6/2, [0, 35], 4.8675*10**24, (255, 128, 0), "Venus")
                earth = Planet([center_w - 152.1, center_h], 6.3/2, [0, 29.3], 5.972*10**24, (0, 0, 255), "Earth")
                mars = Planet([center_w - 228, center_h], 3.5/2, [0, 21.972], 6.4185*10**23, (255, 0, 0), "Mars")
                planets = [sun, mercury, venus, earth, mars]

    pygame.display.update()

pygame.quit()