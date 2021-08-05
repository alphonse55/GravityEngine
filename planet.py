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
        self.future_pos = 0
        self.future_v = 0
        self.points = {}

    def planet_acceleration(self, planets, time="present"):
        a = [0, 0]
        for p in planets:
            if p != self:
                if time == "present":
                    pos1 = self.pos
                    pos2 = p.pos
                elif time == "future":
                    pos1 = self.future_pos
                    pos2 = p.future_pos

                dx = (pos1[0] - pos2[0])*1000000
                dy = (pos1[1] - pos2[1])*1000000

                if dx != 0 or dy != 0:
                    acc = 6.67408*10**-11 * p.m/(dx**2 + dy**2)
                if dx != 0:
                    alfa = math.atan(abs(dy/dx))
                else:
                    alfa = math.pi/2
                    
                if pos2[0] > pos1[0]:
                    a[0] += acc*math.cos(alfa)
                else:
                    a[0] -= acc*math.cos(alfa)

                if pos2[1] > pos1[1]:
                    a[1] += acc*math.sin(alfa)
                else:
                    a[1] -= acc*math.sin(alfa)
        return a

    def update_velocity(self, planets, FPS, v_simulation):
        a = self.planet_acceleration(planets)

        self.v[0] += a[0]/1000/FPS*v_simulation
        self.v[1] += a[1]/1000/FPS*v_simulation

    def update_position(self, FPS, v_simulation):
        self.pos[0] += self.v[0]/FPS*v_simulation
        self.pos[1] += self.v[1]/FPS*v_simulation

        self.points[self.pos[0]] = self.pos[1]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.r)
    
    def write(self, i, screen, font, WIDTH):
        self.vel = (self.v[0]**2 + self.v[1]**2) ** (1/2)

        text_render = font.render(f"{self.name} : {round(self.vel, 2)} km/s (x: {round(self.v[0], 2)}, y: {round(self.v[1], 2)})", True, self.color)
        text_rect = text_render.get_rect(topleft = (WIDTH + 10, 10 + i*30))
        screen.blit(text_render, text_rect)

    def draw_way(self, screen):
        for x in self.points:
            pygame.draw.circle(screen, self.color, (x, self.points[x]), 1)