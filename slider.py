import pygame

class Slider:
    def __init__(self, width, height, topleft, color_line, color_circle, background, min_value, max_value, value):
        self.width = width
        self.height = height
        self.topleft = topleft
        self.color_line = color_line
        self.color_circle = color_circle
        self.background = background
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.pressed = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.background, (self.topleft[0] - self.height, self.topleft[1] - self.height/2, self.width + 2*self.height, 2*self.height)) # cover the old slider
        pygame.draw.rect(screen, self.color_line, (self.topleft[0], self.topleft[1], self.width, self.height), border_radius = int(self.height/2)) # line
        pygame.draw.circle(screen, self.color_circle, (self.topleft[0] + (self.value - self.min_value)/(self.max_value - self.min_value)*self.width, self.topleft[1] + self.height/2), self.height) # cicle

    def mouse_on_circle(self, mouse):
        return abs(self.topleft[0] + (self.value - self.min_value)/(self.max_value - self.min_value)*self.width - mouse[0]) < 2*self.height and abs(self.topleft[1] + self.height/2 - mouse[1]) < 2 * self.height

    def get_value(self, mouse):
        value = (mouse[0] - self.topleft[0]) * self.max_value / self.width
        if value < self.min_value:
            return self.min_value
        elif value > self.max_value:
            return self.max_value
        return value

    def set_value(self, value):
        if value < self.min_value:
            value = self.min_value
        elif value > self.max_value:
            value = self.max_value
        self.value = value