
from distutils.command.config import config
import pygame

import scene

import drivers

class Game:
    def __init__(self):
        self.window_size = pygame.display.get_surface().get_size()
        yaml = drivers.yaml.yaml_driver.YamlDriver()
        self.config = yaml.read(read_file='data/scene/game.yml')
    
    def renderer(self):
        surface = pygame.Surface((self.window_size[0],self.window_size[1])).convert_alpha()
        surface.fill((0,0,0,0))
        surface.blit(pygame.image.load('assets/icon/icon.png'), (0,0))
        
        return surface
    
    def scene_event(self,event):
        pass