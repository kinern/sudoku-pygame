import pygame
from pygame.locals import *

class Button():
        def __init__(self, text,  pos, size, font, onClick, fontColor="White", bg="black"):
            self.x, self.y = pos
            self.font = pygame.font.SysFont("Verdana", font)
            self.onClick = onClick
            self.text = self.font.render(text, 1, pygame.Color(fontColor))
            self.size = size
            self.surface = pygame.Surface(self.size)
            self.surface.fill(bg)
            self.surface.blit(self.text, (int(self.size[0]/2)-int(self.text.get_rect().width/2), int(self.size[1]/2)-int(self.text.get_rect().height/2)))
            self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
    
        #def show(self):
        #    screen.blit(self.surface, (self.x, self.y))
    
        def click(self, event):
            x, y = pygame.mouse.get_pos()
            if self.rect.collidepoint(x, y):
                self.onClick()