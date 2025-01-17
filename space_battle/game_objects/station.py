import pygame_gui
from settings import *
from image_mosaic import ImageMosaic

class Station:
    def __init__(self, data, ships, weapons, image_loader):
        self.pos = pg.Vector2(data["pos"])
        self.size = pg.Vector2(data["size"])
        self.exit_pos = pg.Vector2(data["exit_pos"])

        image = pg.transform.scale(image_loader.stations[data["image_id"]], self.size)
        self.image_mosaic = ImageMosaic(image, data["mosaic_splitting"])

        self.manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), theme_path="ui_theme.json")

        self.weapon_options = weapons
        self.weapon_buttons = self.generate_buttons((150, 400), [weapon.name for weapon in weapons])
        self.ship_options = ships
        self.ship_images = image_loader.ships
        self.thruster_images = image_loader.thruster_flames
        self.ship_buttons = self.generate_buttons((1450, 330), [ship["name"] for ship in ships])
        
        self.repair_button = pygame_gui.elements.UIButton(relative_rect=pg.Rect((1400, 620), (160, 40)), text="repair ship", manager=self.manager)

        self.info_rect = pg.Rect(WINDOW_SEMI_WIDTH - 140, WINDOW_HEIGHT - 260, 280, 240)
        self.info_box = self.get_info_box()

        self.weapons_text_box = pygame_gui.elements.UITextBox("Weapons", pg.Rect((150, 350), (160, 30)), self.manager)
        self.ships_text_box = pygame_gui.elements.UITextBox("Ships", pg.Rect((1450, 280), (160, 30)), self.manager)

        self.font = pg.font.SysFont("Arial", 16)
    
    def generate_buttons(self, start_pos, names):
        buttons = []
        for i in range(len(names)):
            name = names[i]
            buttons.append(pygame_gui.elements.UIButton(relative_rect=pg.Rect(pg.Vector2(start_pos) + pg.Vector2(0, 60 * i), (160, 40)), text=name, manager=self.manager))
        return buttons
    
    def draw(self, window, camera):
        apparent_size = camera.zoom * self.size
        rect = pg.Rect((0, 0), apparent_size)
        rect.center = camera.screen_coords(self.pos.x, self.pos.y)
        if rect.right > 0 and rect.left < WINDOW_WIDTH and rect.bottom > 0 and rect.top < WINDOW_HEIGHT:
            #image = self.template_image
            #image = pg.transform.scale(image, apparent_size)

            #window.blit(image, rect)
            self.image_mosaic.draw(window, rect.topleft, camera.zoom)
    
    def update(self, player, event, delta_t):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            for i in range(len(self.weapon_options)):
                button = self.weapon_buttons[i]
                if event.ui_element == button:
                    player.weapon = self.weapon_options[i] #change weapon
            
            for i in range(len(self.ship_options)):
                button = self.ship_buttons[i]
                if event.ui_element == button:
                    self.change_ship(player, self.ship_options[i]) #change ship
            
            if event.ui_element == self.repair_button:
                player.health = player.max_health #repair ship
        
        if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
            for i in range(len(self.weapon_options)):
                button = self.weapon_buttons[i]
                if event.ui_element == button:
                    weapon = self.weapon_options[i]
                    self.show_weapon_info(weapon) #show info about weapon
            
            for i in range(len(self.ship_options)):
                button = self.ship_buttons[i]
                if event.ui_element == button:
                    ship = self.ship_options[i]
                    self.show_ship_info(ship) #show info about ship
        
        self.manager.process_events(event)

        self.manager.update(delta_t / 1000)
    
    def show_info(self):
        return "station"
    
    def get_info_box(self, text=""):
        return pygame_gui.elements.UITextBox(text, relative_rect=self.info_rect, manager=self.manager)
    
    def show_weapon_info(self, weapon):
        info = f"damage: {weapon.damage}\nrange: {weapon.range}m\nspeed: {weapon.speed * 1000}m/s\nshoot delay: {weapon.delay / 1000}s\ncapacitor usage: {weapon.power_usage}MJ"
        
        self.info_box.kill()
        self.info_box = self.get_info_box(info)
    
    def show_ship_info(self, ship):
        info = "health: " + str(ship["health"]) + "\ncapacitor: " + str(ship["capacitor"]) + "MJ\ncapacitor charge rate: " + str(ship["charge_rate"] * 1000) + "MW\nacceleration: " + str(ship["acceleration"] * 1000000) + "m/s^2\nangular acceleration: " + str(ship["angular_acc"] * 1000000) + "deg/s^2\nmass: " + str(ship["mass"]) + " tonnes\ndimensions:\n  length: " + str(ship["dimensions"]["semi_length"] * 2) + "m\n  width: " + str(ship["dimensions"]["semi_width"] * 2) + "m\ndescription: " + ship["description"]
        
        self.info_box.kill()
        self.info_box = self.get_info_box(info)
    
    def change_ship(self, player, ship):
        player.health = ship["health"]
        player.max_health = ship["health"]

        player.capacitor = ship["capacitor"]
        player.max_capacity = ship["capacitor"]

        player.charge_rate = ship["charge_rate"]

        player.acceleration = ship["acceleration"]

        player.angular_acc = pi / 180 * ship["angular_acc"]

        player.mass = ship["mass"]

        player.hitbox_semi_length = ship["dimensions"]["semi_length"]
        player.hitbox_semi_width = ship["dimensions"]["semi_width"]
        
        player.template_image = self.ship_images[ship["name"]]

        player.thruster_data = ship["thruster_data"]
        player.thruster_flame_image = self.thruster_images[ship["thruster_type"]]