from settings import *
from world_objects import WorldObjects
from main_menu import MainMenu
from save_menu import SaveMenu
from pause_menu import PauseMenu
from locations_menu import LocationsMenu
from image_loader import ImageLoader
from ui import UI
from mini_map import MiniMap
from game_objects.weapon import Weapon

class Main:
    def __init__(self):
        self.running = True

        pg.init()
        self.window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pg.SCALED | pg.RESIZABLE)

        self.image_loader = ImageLoader()

        with open(join("locations.json")) as file: self.locations = json.load(file)
        with open(join("game_objects", "ship_types.json")) as file: self.ship_types = json.load(file)
        with open(join("game_objects", "enemy_types.json")) as file: self.enemy_types = json.load(file)
        self.weapon_types = self.load_weapons(self.image_loader.projectiles)

        self.save_data: dict = None
        self.world_objects: WorldObjects = None

        self.mini_map: MiniMap = None

        self.ui: UI = None
        
        self.clock = pg.time.Clock()
        self.delta_t = 0

        self.main_menu = MainMenu()
        self.mainmenu_active = True

        self.save_menu = SaveMenu()
        self.savemenu_active = False

        self.pause_menu = PauseMenu()
        self.pause = False

        self.locations_menu = LocationsMenu(self.locations)
        self.locationsmenu_active = False

        self.pause_bg = pg.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

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
            if event.type == pg.MOUSEBUTTONDOWN:
                self.scroll_forward = event.button == 4 #scroll forward
                
                self.scroll_back = event.button == 5 #scroll back
                
                self.lmb_pressed = event.button == 1
            
            elif event.type == pg.MOUSEBUTTONUP:
                self.lmb_pressed = False
            
            elif event.type == pg.QUIT:
                self.world_objects.save()
                self.running = False
            
            elif event.type == pg.FULLSCREEN:
                pg.display.toggle_fullscreen()
    
    def peform_actions(self):
        if self.key_state_just_pressed[pg.K_ESCAPE] and not self.mainmenu_active:
            self.pause = not self.pause #pause/unpause
            if self.pause: self.pause_bg = self.window.copy()
        
        if self.key_state_just_pressed[pg.K_t] and not (self.pause or self.mainmenu_active or self.savemenu_active) :
            self.locationsmenu_active = not self.locationsmenu_active
            if self.locationsmenu_active: self.pause_bg = self.window.copy()
    
    @staticmethod
    def load_weapons(images):
        weapons = []
        with open(join("game_objects", "weapon_types.json")) as file:
            data = json.load(file)
            for w in data:
                weapons.append(Weapon(w["name"], w["damage"], w["electronic_damage"], w["speed"], w["delay"], w["range"], w["power_usage"], w["mass"], w["projectile_mass"], images[w["image_id"]]))
        return weapons

    def load_world(self, save_data, save_name):
        self.save_data = save_data
        self.world_objects = WorldObjects(self, save_data, save_name)
        self.mini_map = MiniMap(self.world_objects)
        self.ui = UI(self.world_objects.player)
        self.savemenu_active = False
    
    def run(self):
        while self.running:
            self.delta_t = self.clock.tick(60)

            self.detect_key_presses()
            self.check_events()
            self.peform_actions()
            
            if self.mainmenu_active:
                #main menu
                self.window.fill((0, 0, 0))
                self.main_menu.update(self)
            elif self.savemenu_active:
                self.window.fill((0, 0, 0))
                self.save_menu.update(self)
            elif self.pause:
                #paused
                self.window.blit(self.pause_bg, (0, 0))
                self.pause_menu.update(self)
            elif self.locationsmenu_active:
                #locations menu
                self.window.blit(self.pause_bg, (0, 0))
                self.locations_menu.update(self)
            else:
                #game
                self.window.blit(self.image_loader.bg_images[self.world_objects.bg_image_id], (0, 0)) #draw background
                self.world_objects.update(self.delta_t)
                self.ui.draw(self.window, self.world_objects.camera)
                self.mini_map.update(self.key_state_pressed, self.key_state_just_pressed, self.scroll_forward, self.scroll_back)
                if self.world_objects.player.docked: self.world_objects.station.update_ui(self, self.world_objects.player)

            pg.display.flip()

if __name__ == "__main__":
    #dir_path = os.path.realpath(os.path.dirname(__file__))
    #os.chdir(dir_path)
    
    app = Main()
    app.run()