from settings import *

class MiniMap:
    def __init__(self, world_objects):
        self.corner_size = (300, 300)
        self.expanded_size = (1700, 930)
        self.offset = pg.Vector2(10, 10)
        self.map = pg.surface.Surface(self.corner_size)
        
        self.map.set_alpha(204)

        self.max_scale = 0.029
        self.min_scale = 0.011
        self.scale = self.max_scale #size scale factor from world to map

        self.world_objects = world_objects

        self.font = pg.font.SysFont("Arial", 16)
    
    def update(self, key_state_pressed, key_state_just_pressed, scroll_forward, scroll_back):
        self.draw()
        if key_state_just_pressed[pg.K_m]:
            self.change_size()
        
        if key_state_pressed[pg.K_LCTRL]:
            if scroll_forward:
                self.zoom_in()
            elif scroll_back:
                self.zoom_out()
    
    def draw_border(self):
        #draws yellow border around map
        size = self.map.get_size()
        corners = (
            (0, 0),
            (0, size[1] - 1),
            (size[0] - 1, size[1] - 1),
            (size[0] - 1, 0)
        )
        for i in range(4):
            pg.draw.line(self.map, (255, 255, 0), corners[i], corners[(i + 1) % 4])
    
    def draw_on_map(self, obj, colour, focus_pos, radius): #function for drawing on map. translates world coords into map coords
        map_pos = self.scale * (obj.pos - focus_pos - pg.Vector2(WINDOW_SEMI_WIDTH, WINDOW_SEMI_HEIGHT)) + pg.Vector2(self.map.get_size()) // 2
        pg.draw.circle(self.map, colour, map_pos, radius)

        #show info about object if cursor hovers over it
        if pg.Vector2(pg.mouse.get_pos() - map_pos - self.offset).magnitude_squared() < radius * radius:
            text_surf = self.font.render(obj.show_info(), False, (255, 255, 255))
            self.map.blit(text_surf, map_pos - pg.Vector2(radius))
    
    def change_size(self):
        if self.map.get_size() == self.corner_size:
            #expand map to fill screen
            self.map = pg.transform.scale(self.map, self.expanded_size)
            self.offset = pg.Vector2(0, 0)
        else:
            #collapse map back into corner
            self.map = pg.transform.scale(self.map, self.corner_size)
            self.offset = pg.Vector2(10, 10)
    
    def zoom_in(self):
        self.scale = min(self.scale * ZOOM_RATE, self.max_scale)
    
    def zoom_out(self):
        self.scale = max(self.scale / ZOOM_RATE, self.min_scale)
    
    def draw(self):
        self.map.fill((0, 0, 0))
        
        for bs in self.world_objects.battle_sites:
            #draw battle sites
            self.draw_on_map(bs, (57, 57, 57), self.world_objects.camera.focus_pos, self.scale * BATTLE_SITE_RADIUS)

            for ene in bs.enemies:
                #draw enemies
                self.draw_on_map(ene, (255, 0, 0), self.world_objects.camera.focus_pos, 6)
            
            for hlthup in bs.hlthUps:
                #draw healthups
                self.draw_on_map(hlthup, (231, 231, 252), self.world_objects.camera.focus_pos, 4)
        
        #draw player
        self.draw_on_map(self.world_objects.player, (0, 255, 0), self.world_objects.camera.focus_pos, 6)

        #draw station
        self.draw_on_map(self.world_objects.station, (150, 45, 18), self.world_objects.camera.focus_pos, 10)
        
        self.draw_border()

        self.world_objects.app.window.blit(self.map, self.offset)