import math
import random
import pygame
from PIL import Image

from planet import Planet
from solar_system import SolarSystem
from slider import Slider

pygame.init()

width_data_rect = 300
WIDTH = int(pygame.display.Info().current_w * 5/6) - width_data_rect
HEIGHT = int(pygame.display.Info().current_h * 5/6)

screen = pygame.display.set_mode((WIDTH + width_data_rect, HEIGHT)) 
pygame.display.set_caption("Gravity Engine")

center_w = WIDTH/2
center_h = HEIGHT/2

SKY_BLUE = (0, 0, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

FPS = 100
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)

number_keys = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

color_hue = pygame.image.load("color_hue.png")
color_hue_pixels = list(Image.open("color_hue.png").getdata())

num_stars = 100
stars = [(screen, tuple([random.randint(150, 250)]*3), (random.randint(0, WIDTH), random.randint(0, HEIGHT)), random.randint(1, 3)) for i in range(num_stars)]

v_simulation = 10
max_v_simulation = 20

slider = Slider(2/3 * width_data_rect, 10, (WIDTH + width_data_rect/6, HEIGHT - 75), RED, WHITE, BLACK, 1, max_v_simulation, v_simulation)

def solar_system():
    # distance : in millions of km
    # radius : in thousands of km, all get divided by 2 and the sun by 10 on top for size on screen, then divided by 1000 to make it fit
    # velocity : in km/s
    # mass : in kg
    sun = Planet([center_w, center_h], 696.340/20, [0, 0], 1.989*10**30, (255, 255, 0), "Sun")
    mercury = Planet([center_w - 69.8, center_h], 2.439, [0, 38.86], 3.301*10**23, (128, 128, 128), "Mercury")
    venus = Planet([center_w - 108, center_h], 6.051, [0, 35], 4.8675*10**24, (255, 128, 0), "Venus")
    earth = Planet([center_w - 152.1, center_h], 6.371, [0, 29.3], 5.972*10**24, BLUE, "Earth")
    mars = Planet([center_w - 228, center_h], 3.390, [0, 21.972], 6.4185*10**23, RED, "Mars")

    m = 1.5*10**29
    x = 97.000436
    y = 24.308753
    vx = 9.3240737
    vy = 8.6473146
    p1 = Planet([center_w + x, center_h + y], 10, [vx/2, -vy/2], m, BLUE)
    p2 = Planet([center_w - x, center_h - y], 10, [vx/2, -vy/2], m, RED)
    p3 = Planet([center_w, center_h], 10, [-vx, vy], m, WHITE)

    # planets = [p1, p2, p3] # 8 figure
    planets = [sun, mercury, venus, mars, earth] # solar system
    return planets, SolarSystem(planets)

planets, system = solar_system()

game = True

while game:
    screen.fill(SKY_BLUE)

    for star in stars:
        pygame.draw.circle(*star)

    # for planet in planets:
    #     for p in planets:
    #         if p != planet:
    #             if (p.pos[0]-planet.pos[0])**2 + (p.pos[1]-planet.pos[1])**2 < (p.r + planet.r)**2:
                    
    #                 if planet.r > p.r:
    #                     pos = planet.pos
    #                 else:
    #                     pos = p.pos

    #                 r = (p.r**3 + planet.r**3)**(1/3)

    #                 m = p.m+planet.m

    #                 v_x = (p.m*p.v[0] + planet.m * planet.v[0])/m
    #                 v_y = (p.m*p.v[1] + planet.m * planet.v[1])/m
    #                 v = [v_x, v_y]

    #                 red = int((p.color[0]*p.m + planet.color[0]*planet.m)/m)
    #                 green = int((p.color[1]*p.m + planet.color[1]*planet.m)/m)
    #                 blue = int((p.color[2]*p.m + planet.color[2]*planet.m)/m)
    #                 color = (red, green, blue)

    #                 planets.append(Planet(pos, r, v, m, color))
    #                 planets.remove(p)
    #                 planets.remove(planet)
    #                 break
    #     else:
    #         continue
    #     break

    for planet in planets:
        planet.update_velocity(planets, FPS, v_simulation)

    for planet in planets:
        planet.update_position(FPS, v_simulation)
        planet.draw(screen)

    pygame.draw.rect(screen, BLACK, (WIDTH, 0, width_data_rect, HEIGHT))
    pygame.draw.line(screen, WHITE, (WIDTH, 0), (WIDTH, HEIGHT))

    for i in range(len(planets)):
        planets[i].write(i, screen, font, WIDTH)
    
    slider.set_value(v_simulation)
    slider.draw(screen)

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x < WIDTH:
                planet_pos = planet_w, planet_h = pygame.mouse.get_pos()
                
                rect_w, rect_h = 100, 20

                mass = "1*10**23"
                color = WHITE

                done = False
                esc = False
                confirm = False

                while not confirm:
                    mouse = mouse_x, mouse_y = pygame.mouse.get_pos()

                    if not done:
                        screen.fill(SKY_BLUE)

                        for star in stars:
                            pygame.draw.circle(*star)

                        for planet in planets:
                            planet.draw(screen)

                        try:
                            m = eval(mass) # instead of eval(), I could use the solve() function from my calculator
                        except:
                            pass

                        # if m < 10**24:
                        #     radius = 1
                        # elif m < 10**25:
                        #     radius = 3
                        # elif m < 10**27:
                        #     radius = 5
                        # elif m < 10**30:
                        #     radius = 10
                        # else:
                        #     radius = math.log(m, 10)

                        radius = 10

                        vel = [(mouse_x-planet_w)/10, (mouse_y-planet_h)/10]

                        pygame.draw.line(screen, RED, planet_pos, mouse, 3)
                        dx = mouse_x - planet_w
                        dy = planet_h - mouse_y
                        if dx != 0 and dy != 0:
                            x = planet_w + dx*0.95
                            y = planet_h - dy*0.95
                            x1 = x+dy*0.03
                            y1 = y+dx*0.03
                            x2 = x-dy*0.03
                            y2 = y-dx*0.03
                            pygame.draw.polygon(screen, RED, [mouse, (x1, y1), (x2, y2)])
                        
                        try:
                            p = Planet([planet_w, planet_h], radius, vel, m, color)
                        except:pass
                        p.draw(screen)

                        system.predict(screen, FPS, 60, p)

                        pygame.draw.rect(screen, BLACK, (WIDTH, 0, width_data_rect, HEIGHT))
                        pygame.draw.line(screen, WHITE, (WIDTH, 0), (WIDTH, HEIGHT))

                        for i in range(len(planets)):
                            planets[i].write(i, screen, font, WIDTH)
                        
                        p.write(i+1, screen, font, WIDTH)

                        if (planet_w < WIDTH - 5 - rect_w + radius) and (planet_h > rect_h + 5 + radius):
                            rect = (planet_w - radius, planet_h - rect_h - radius - 5, rect_w, rect_h)
                            mass_render = font.render(mass, True, BLACK)
                            mass_rect = mass_render.get_rect(center = (planet_w - radius + rect_w/2, planet_h - rect_h - radius - 5 + rect_h/2))

                        elif (planet_h > rect_h + 5 + radius): # too far right
                            rect = (min(planet_w - rect_w + radius, WIDTH - 5 - rect_w), planet_h - rect_h - radius - 5, rect_w, rect_h)
                            mass_render = font.render(mass, True, BLACK)
                            mass_rect = mass_render.get_rect(center = (min(planet_w - rect_w + radius, WIDTH - 5 - rect_w) + rect_w/2, planet_h - rect_h - radius - 5 + rect_h/2))
                        
                        else: # top-right corner
                            rect = (min(planet_w - rect_w + radius, WIDTH - 5 - rect_w), planet_h + radius + 5, rect_w, rect_h)
                            mass_render = font.render(mass, True, BLACK)
                            mass_rect = mass_render.get_rect(center = (min(planet_w - rect_w + radius, WIDTH - 5 - rect_w) + rect_w/2, planet_h + radius + 5 + rect_h/2))
                        
                        pygame.draw.rect(screen, WHITE, rect, border_radius = 5)
                        screen.blit(mass_render, mass_rect)

                    else:
                        point = (10, 10)
                        width = 10
                        if planet_w < 300 and planet_h < 300:
                            point = (10, HEIGHT - 10 - 2 * width - 255)
                        pygame.draw.rect(screen, (0, 0, 0), (*point, 255 + 2 * width, 255 + 2 * width), border_radius = 5)
                        screen.blit(color_hue, (point[0] + width, point[1] + width, 255, 255))

                        if (point[0] + width < mouse_x < point[0] + width + 255) and (point[1] + width < mouse_y < point[1] + width + 255):
                            pixel_x = mouse_x - width - point[0]
                            pixel_y = mouse_y - width - point[1]
                            color = color_hue_pixels[pixel_y * 255 + pixel_x]
                            pygame.draw.circle(screen, color, mouse, 10)
                            pygame.draw.circle(screen, BLACK, mouse, 10, 1)

                            p = Planet([planet_w, planet_h], radius, vel, eval(mass), color)
                            p.draw(screen)

                            pygame.draw.rect(screen, WHITE, rect, border_radius = 5)
                            screen.blit(mass_render, mass_rect)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if not done:
                                if eval(mass) < 10**35:
                                    done = True
                                else:
                                    mass = "1*10**23"
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

                    slider.draw(screen)

                    pygame.display.update()

                if not esc:
                    planets.append(Planet(list(planet_pos), radius, vel, m, color)) 
                    system.planets = planets

            elif slider.mouse_on_circle(mouse):
                slider.pressed = True
                while slider.pressed:
                    mouse = pygame.mouse.get_pos()
                    slider.value = slider.get_value(mouse)
                    slider.draw(screen)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            slider.pressed = False
                            slider.value = slider.get_value(mouse)
                            v_simulation = slider.value

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                planets, system = solar_system()
            elif event.key == pygame.K_SPACE:
                if v_simulation > 0:
                    old_v_simulation = v_simulation
                    v_simulation = 0
                else:
                    v_simulation = old_v_simulation

    pygame.display.update()

pygame.quit()