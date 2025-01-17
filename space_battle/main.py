import os
import json
from settings import *
from world_objects import WorldObjects
from pause_menu import PauseMenu
from image_loader import ImageLoader
from ui import UI
from mini_map import MiniMap

class Main:
    def __init__(self):
        self.running = True
        self.pause = False

        pg.init()
        self.window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pg.SCALED | pg.RESIZABLE)

        self.image_loader = ImageLoader()

        with open("locations.json") as file:
            self.locations = json.load(file)

        self.world_objects = WorldObjects(self, self.locations[0])

        self.mini_map = MiniMap(self.world_objects)
        
        self.clock = pg.time.Clock()
        self.delta_t = 0

        self.pause_menu = PauseMenu()

        self.ui = UI(self.world_objects.player)

        self.lmb_pressed = False
        self.scroll_forward = False
        self.scroll_back = False

    #KEY HANDLING
    def detect_key_presses(self):
        self.key_state_pressed = pg.key.get_pressed()
        self.key_state_just_pressed = pg.key.get_just_pressed()
        self.key_mods = pg.key.get_mods()
    
    def check_events(self):
        self.scroll_forward = False
        self.scroll_back = False
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN and not self.pause:
                self.scroll_forward = event.button == 4 #scroll forward
                
                self.scroll_back = event.button == 5 #scroll back
                
                self.lmb_pressed = event.button == 1
            
            elif event.type == pg.MOUSEBUTTONUP and not self.pause:
                self.lmb_pressed = False
            
            elif event.type == pg.QUIT:
                self.running = False
            
            elif event.type == pg.FULLSCREEN:
                pg.display.toggle_fullscreen()
            
            if self.pause:
                self.pause_menu.update(self, event)
            
            if self.world_objects.player.docked:
                self.world_objects.station.update(self.world_objects.player, event, self.delta_t)

    def run(self):
        while self.running:
            self.delta_t = self.clock.tick(60)

            self.detect_key_presses()
            self.check_events()
            if self.key_state_just_pressed[pg.K_ESCAPE]:
                self.pause = not self.pause #pause/unpause
            
            if not self.pause:
                self.window.blit(self.image_loader.bg_images[self.world_objects.bg_image_id], (0, 0)) #draw background
                self.world_objects.update(self.delta_t)
            
            self.ui.draw(self.window, self.world_objects.camera)

            if not self.pause:
                self.mini_map.update(self.key_state_pressed, self.key_state_just_pressed, self.scroll_forward, self.scroll_back)

            pg.display.flip()

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    
    app = Main()
    app.run()