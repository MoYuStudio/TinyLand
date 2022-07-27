
import pygame

import engine
import scene

import drivers

class Game:
    def __init__(self):
        self.window_size = pygame.display.get_surface().get_size()
        yaml_file = drivers.yaml.yaml_driver.YamlDriver()
        self.config = yaml_file.read(read_file='data/scene/game.yml')
        
        json_file = drivers.json.json_driver.JsonDriver()
        self.map = json_file.read(read_file='data/map')
        
        self.size = 4
        self.tilemap_obj = engine.tilemap.Tilemap(self.map['map'],self.size)
        
    
    def renderer(self):
        surface = pygame.Surface((self.window_size[0],self.window_size[1])).convert_alpha()
        surface.fill((0,0,0,0))
        
        surface.blit(pygame.image.load('assets/icon/icon.png'), (0,0))
        
        self.tilemap_obj.renderer(surface)
        
        return surface
    
    def scene_event(self,event):
        pass