
import glob
import pygame

import drivers

class Tile:
    def __init__(self,pos,id,size):
        self.pos = pos
        self.id = id
        self.size = size
        
        self.timer_list = {'grow':0,'animation':0}
        self.animation_frame = 0
        self.render_id = self.id
        self.offset = [0,0]
        
        yaml = drivers.yaml.yaml_driver.YamlDriver()
        self.config = yaml.read(read_file='data/engine/tile.yml')
        
        try:
            self.tile_data = yaml.read(read_file=self.config['tile_data'])
        except:
            print('Engine/Object:Tile (tile_data) Missing')
            pass
        
    def renderer(self,surface):
        try:
            self.assets_original = pygame.image.load(self.config['assets_original']+str(self.render_id)+'.png')
            self.assets = pygame.transform.scale(self.assets_original,(16*self.size, 16*self.size))
            
            self.rect = self.assets.get_rect()
            self.width = self.rect.width
            
            self.mask_original = pygame.image.load(self.config['mask_original']).convert_alpha()
            self.mask = pygame.transform.scale(self.mask_original,((self.width,self.width)))
            
            the_tile_data = self.tile_data[self.id]
            
            for type in self.timer_list:
                try:
                    if self.timer_list[type] >= the_tile_data[type+'_timer']:
                        self.timer_list[type] = 0
                        
                        if type == 'grow':
                            self.id = the_tile_data['grow_next']
                            self.render_id = self.id
                        if type == 'animation':
                            if self.animation_frame >= the_tile_data['animation_frame']:
                                self.animation_frame = 0
                                self.render_id = str(self.id)
                            else:
                                self.animation_frame += 1
                                self.render_id = str(self.id)+'a'+str(self.animation_frame)
                    else:
                        self.timer_list[type] += 1
                except:
                    pass
            
            self.rect.x = self.pos['z']*(self.width/2)-self.pos['x']*(self.width/2)+self.offset[0]
            self.rect.y = self.pos['x']*(self.width/4)+self.pos['z']*(self.width/4)+self.offset[1]+(-self.width/2)*int(self.pos['y'])
            
            surface.blit(self.assets, self.rect)
            
            return self.rect
            
        except:
            pass
            # print('Engine/Object:Tile [renderer] Erro')
        
    def touch(self,change_tile):
        if self.pos['y'] == '1':
            touch_rect = self.rect.copy()
            touch_rect.y = touch_rect.y + touch_rect.height/2
            
            pos = pygame.mouse.get_pos()
            tile_mask = pygame.mask.from_surface(self.mask)
            pos_in_mask = (pos[0]-touch_rect.x),(pos[1]-touch_rect.y)
            touching = touch_rect.collidepoint(*pos) and tile_mask.get_at(pos_in_mask)
            
            if pygame.mouse.get_pressed()[0] == True:
                if touching == True:
                    if self.id == 0:
                        self.id = change_tile