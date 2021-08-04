import math
import pygame

class Planet:
    def __init__(self, pos, r, v, m, color, name = "Planet"):
        self.name = name
        self.pos = pos
        self.r = r
        self.v = v
        self.m = m
        self.color = color

    def update(self, planets, FPS):
        a = [0, 0]
        for p in planets:
            if p != self:
                dx = (self.pos[0] - p.pos[0])*1000*1000
                dy = (self.pos[1] - p.pos[1])*1000*1000

                if dx != 0 or dy != 0:
                    acc = 6.67408*10**-11 * p.m/(dx**2 + dy**2)
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

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.r)
    
    def write(self, i, screen, font, WIDTH):
        self.vel = (self.v[0]**2 + self.v[1]**2) ** (1/2)

        text_render = font.render(f"{self.name} : {round(self.vel, 2)} km/s (x: {round(self.v[0], 2)}, y: {round(self.v[1], 2)})", True, self.color)
        text_rect = text_render.get_rect(topleft = (WIDTH + 10, 10 + i*30))
        screen.blit(text_render, text_rect)