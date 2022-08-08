
import pygame

import engine
import scene

import drivers

class Game:
    def __init__(self):
        self.window_size = pygame.display.get_surface().get_size()
        yaml_file = drivers.yaml.yaml_driver.YamlDriver()
        self.config = yaml_file.read(read_file='data/scene/game.yml')
        
        json_file = drivers.json.json_driver.JsonDriver(path='data/map')
        self.map = json_file.read()
        
        self.size = 4
        self.tilemap_obj = engine.tilemap.Tilemap(self.map['1'],self.size)
        
        self.tilemap_offset = [self.window_size[0]/self.size/2,self.window_size[1]/self.size/2]
        self.move_speed = 3
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        
        self.tile_pick = 262
    
    def renderer(self):
        
        if self.move_up == True:
            self.tilemap_offset[1] -= self.move_speed
        if self.move_down == True:
            self.tilemap_offset[1] += self.move_speed
        if self.move_left == True:
            self.tilemap_offset[0] -= self.move_speed
        if self.move_right == True:
            self.tilemap_offset[0] += self.move_speed
        
        surface = pygame.Surface((self.window_size[0],self.window_size[1])).convert_alpha()
        surface.fill((0,0,0,0))
        
        self.tilemap_obj.renderer(surface,self.tilemap_offset)
        
        return surface
    
    def scene_event(self,event):
        self.event = event
        if self.event.type == pygame.MOUSEBUTTONDOWN:
                
            self.tilemap_obj.touch(self.tile_pick, pos_offset=self.tilemap_offset)
        
        if self.event.type == pygame.KEYDOWN:
            if self.event.key == pygame.K_UP or self.event.key == pygame.K_w:
                self.move_up = True
            if self.event.key == pygame.K_DOWN or self.event.key == pygame.K_s:
                self.move_down = True
            if self.event.key == pygame.K_LEFT or self.event.key == pygame.K_a:
                self.move_left = True
            if self.event.key == pygame.K_RIGHT or self.event.key == pygame.K_d:
                self.move_right = True
                
        if self.event.type == pygame.KEYUP:
            if self.event.key == pygame.K_UP or self.event.key == pygame.K_w:
                self.move_up = False
            if self.event.key == pygame.K_DOWN or self.event.key == pygame.K_s:
                self.move_down = False
            if self.event.key == pygame.K_LEFT or self.event.key == pygame.K_a:
                self.move_left = False
            if self.event.key == pygame.K_RIGHT or self.event.key == pygame.K_d:
                self.move_right = False