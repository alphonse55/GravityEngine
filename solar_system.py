from copy import deepcopy
import pygame

class SolarSystem:
    def __init__(self, planets):
        self.planets = planets
    
    def predict(self, screen, t, p=None):
        FPS = 50
        planets = deepcopy(self.planets)
        if p != None:
            planets.append(p)

        for planet in planets:
            planet.future_pos = planet.pos
            planet.future_v = planet.v

        for _ in range(t*FPS):
            for planet in planets:
                a = planet.planet_acceleration(planets, "future")

                v = deepcopy(planet.future_v)
                v[0] = v[0] + a[0]/1000/FPS
                v[1] = v[1] + a[1]/1000/FPS

                p = deepcopy(planet.future_pos)
                p[0] = p[0] + v[0]/FPS
                p[1] = p[1] + v[1]/FPS

                planet.future_pos = p
                planet.future_v = v

                pygame.draw.circle(screen, planet.color, p, 1)