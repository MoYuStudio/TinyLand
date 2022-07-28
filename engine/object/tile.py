
import glob
import pygame

import drivers

class Tile:
    def __init__(self,pos,id,size):
        self.pos = pos
        self.id = id
        self.size = size
        
        self.timer_timer = {'grow':0,'animation':0}
        self.offset = [0,0]
        
        yaml = drivers.yaml.yaml_driver.YamlDriver()
        self.config = yaml.read(read_file='data/engine/tile.yml')
        self.tile_data = yaml.read(read_file=self.config['tile_data'])
        
        num = []
        for filename in glob.glob(self.config['glob_filename']):
            num.append(filename)
        self.tile_num = len(num)
        
        self.assets_original = [pygame.image.load(self.config['assets_original']+str(i)+'.png')for i in range(0,(self.tile_num),1)]
        self.assets = [pygame.transform.scale(self.assets_original[i],(16*self.size, 16*self.size))for i in range(0,(self.tile_num),1)]
        
        self.rect = self.assets[self.id].get_rect()
        self.width = self.rect.width
        
        self.mask_original = pygame.image.load(self.config['mask_original']).convert_alpha()
        self.mask = pygame.transform.scale(self.mask_original,((self.width,self.width)))
        
    def renderer(self,surface):
        for type in self.timer_timer:
            try:
                timer = self.tile_data[str(self.id)][type+'_timer']
                nextfps = self.tile_data[str(self.id)][type+'_nextfps']
                if timer >= 0:
                    self.timer_timer[type] += 1
                if self.timer_timer[type] == timer:
                    self.id = nextfps
                    self.timer_timer[type] = 0
            
            except:
                pass
        self.rect.x = self.pos['z']*(self.width/2)-self.pos['x']*(self.width/2)+self.offset[0]
        self.rect.y = self.pos['x']*(self.width/4)+self.pos['z']*(self.width/4)+self.offset[1]+(-self.width/2)*int(self.pos['y'])
        
        surface.blit(self.assets[self.id], self.rect)
        
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
                    if self.code == 0:
                        self.code = change_tile