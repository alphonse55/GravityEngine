import pygame

class Slider:
    def __init__(self, name, font, width, height, topleft, color_line, color_circle, background, min_value, max_value, value, full = True):
        self.name_render = font.render(name, True, color_circle)        
        self.width = width
        self.height = height
        self.topleft = topleft
        self.color_line = color_line
        self.color_circle = color_circle
        self.background = background
        self.min_value = min_value
        self.min_value_render = font.render(str(min_value), True, color_circle)
        self.max_value = max_value
        self.max_value_render = font.render(str(max_value), True, color_circle)
        self.value = value

        self.full = full
        self.pressed = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.background, (self.topleft[0] - self.height, self.topleft[1] - self.height/2, self.width + 2*self.height, 2*self.height)) # cover the old slider
        name_rect = self.name_render.get_rect(bottomleft = (self.topleft[0], self.topleft[1] - 20))
        pygame.draw.rect(screen, self.background, name_rect) # cover the old text

        screen.blit(self.name_render, name_rect) # write new text

        width = self.width
        if not self.full: # go only up to the circle
            width *= (self.value-self.min_value)/(self.max_value-self.min_value)
        
        if len(self.color_line) == 3: # RGB values, 1 color
            pygame.draw.rect(screen, self.color_line, (self.topleft[0], self.topleft[1], width, self.height), border_radius = int(self.height/2)) # line with one color
        
        elif len(self.color_line) == 2: # 2 colors
            color = tuple([self.color_line[0][n] + ((self.color_line[1][n] - self.color_line[0][n]) * (self.value-self.min_value)/(self.max_value-self.min_value)) for n in range(3)])
            pygame.draw.rect(screen, color, (self.topleft[0], self.topleft[1], width, self.height), border_radius = int(self.height/2)) # line with two colors
        
        pygame.draw.circle(screen, self.color_circle, (self.topleft[0] + (self.value - self.min_value)/(self.max_value - self.min_value)*self.width, self.topleft[1] + self.height/2), self.height) # circle

        # draw small lines
        pygame.draw.line(screen, self.color_circle, (self.topleft[0], self.topleft[1] + self.height * 2), (self.topleft[0], self.topleft[1] + self.height * 3))
        pygame.draw.line(screen, self.color_circle, (self.topleft[0] + self.width, self.topleft[1] + self.height * 2), (self.topleft[0] + self.width, self.topleft[1] + self.height * 3))

        min_value_rect = self.min_value_render.get_rect(midtop = (self.topleft[0], self.topleft[1] + self.height * 4))
        max_value_rect = self.max_value_render.get_rect(midtop = (self.topleft[0] + self.width, self.topleft[1] + self.height * 4))
        
        # cover old numbers
        pygame.draw.rect(screen, self.background, min_value_rect)
        pygame.draw.rect(screen, self.background, max_value_rect)

        # draw numbers
        screen.blit(self.min_value_render, min_value_rect)
        screen.blit(self.max_value_render, max_value_rect)

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