from settings import *

class Camera:
    def __init__(self):
        self.zoom = 1
        self.focus_pos = pg.Vector2() #world coords
        self.offset = pg.Vector2() #in screen coords, not world coords
    
    def screen_coords(self, x, y):
        return (x - self.focus_pos.x - WINDOW_SEMI_WIDTH) * self.zoom + WINDOW_SEMI_WIDTH, (y - self.focus_pos.y - WINDOW_SEMI_HEIGHT) * self.zoom + WINDOW_SEMI_HEIGHT
    
    def update_offset(self, rel):
        self.offset -= rel
        self.offset.x = max(-WINDOW_SEMI_WIDTH, min(self.offset.x, WINDOW_SEMI_WIDTH))
        self.offset.y = max(-WINDOW_SEMI_HEIGHT, min(self.offset.y, WINDOW_SEMI_HEIGHT))

    def focus(self, focused_obj_pos):
        w = WINDOW_SEMI_WIDTH / self.zoom
        h = WINDOW_SEMI_HEIGHT / self.zoom
        self.focus_pos.x = min(max(focused_obj_pos.x + self.offset.x / self.zoom, w), WORLD_SIZE - w) - WINDOW_SEMI_WIDTH #focus x
        self.focus_pos.y = min(max(focused_obj_pos.y + self.offset.y / self.zoom, h), WORLD_SIZE - h) - WINDOW_SEMI_HEIGHT #focus y
    
    def zoom_in(self):
        self.zoom = min(self.zoom * ZOOM_RATE, MAX_ZOOM)
    
    def zoom_out(self):
        self.zoom = max(self.zoom / ZOOM_RATE, MIN_ZOOM)