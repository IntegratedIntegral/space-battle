from settings import *
from image_mosaic import ImageMosaic
from button import Button
from info_panel import InfoPanel
from paragraph_line_break import line_break

class Station:
    def __init__(self, data, ships, weapons, image_loader):
        self.pos = pg.Vector2(data["pos"])
        self.size = pg.Vector2(data["size"])
        self.exit_pos = pg.Vector2(data["exit_pos"])

        image = pg.transform.scale(image_loader.stations[data["image_id"]], self.size)
        self.image_mosaic = ImageMosaic(image, data["mosaic_splitting"])

        self.weapon_options = weapons
        self.weapon_buttons = self.generate_buttons((190, 400), (220, 40), [weapon.name for weapon in weapons])
        self.ship_options = ships
        self.ship_images = image_loader.ships
        self.thruster_images = image_loader.thruster_flames
        self.ship_buttons = self.generate_buttons((1450, 330), (160, 40), [ship["name"] for ship in ships])
        
        self.repair_button = Button((1400, 620), (160, 40), "repair ship")

        self.info_box = InfoPanel((WINDOW_SEMI_WIDTH - 140, WINDOW_HEIGHT - 370), (280, 360), text_pos=(10, 10), colour=BUTTON_COLOUR, text_colour=UI_TEXT_COLOUR, alpha=255)
        self.info_box_rows = []

        self.weapons_title_box = InfoPanel((190, 350), (220, 30), text_pos=(10, 9), colour=BUTTON_COLOUR, text_colour=UI_TEXT_COLOUR, alpha=255)
        self.ships_title_box = InfoPanel((1450, 280), (160, 30), text_pos=(10, 9), colour=BUTTON_COLOUR, text_colour=UI_TEXT_COLOUR, alpha=255)

        #self.font = pg.font.SysFont("Arial", 16)
    
    def generate_buttons(self, start_pos, size, names):
        buttons = []
        for i in range(len(names)):
            name = names[i]
            buttons.append(Button((start_pos[0], start_pos[1] + 60 * i), size, name))
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
    
    def update_ui(self, app, player):
        self.weapons_title_box.base_draw(app.window, ["weapons"])
        self.ships_title_box.base_draw(app.window, ["Ships"])
        self.repair_button.update(app.window, app.lmb_pressed)

        for i in range(len(self.weapon_options)):
            button = self.weapon_buttons[i]
            weapon = self.weapon_options[i]

            button.update(app.window, app.lmb_pressed)
            if button.pressed: player.weapon = self.weapon_options[i] #change weapon
            if button.hovered: self.show_weapon_info(weapon)
        
        for i in range(len(self.ship_options)):
            button = self.ship_buttons[i]
            ship = self.ship_options[i]

            button.update(app.window, app.lmb_pressed)
            if button.pressed: self.change_ship(player, self.ship_options[i]) #change ship
            if button.hovered: self.show_ship_info(ship)
            
        if self.repair_button.pressed: player.health = player.max_health #repair ship

        self.info_box.base_draw(app.window, self.info_box_rows)
    
    def show_info(self):
        return "station"
    
    def show_weapon_info(self, weapon):
        self.info_box_rows = [
            f"damage: {weapon.damage}",
            f"electronic damage: {weapon.electronic_damage}MJ",
            f"range: {weapon.range}m",
            f"speed: {weapon.speed * 1000}m/s",
            f"shoot delay: {weapon.delay / 1000}s",
            f"capacitor usage: {weapon.power_usage}MJ",
            f"projectile mass: {weapon.mass} tonnes"
        ]
    
    def show_ship_info(self, ship):
        self.info_box_rows = [
            "health: " + str(ship["health"]),
            "capacitor: " + str(ship["capacitor"]) + "MJ",
            "capacitor charge rate: " + str(ship["charge_rate"] * 1000) + "MW",
            "acceleration: " + str(ship["acceleration"] * 1000000) + "m/s^2",
            "angular acceleration: " + str(ship["angular_acc"] * 1000000) + "deg/s^2",
            "mass: " + str(ship["mass"]) + "tonnes",
            "dimensions:",
            "  length: " + str(ship["dimensions"]["semi_length"] * 2) + "m",
            "  width: " + str(ship["dimensions"]["semi_width"] * 2) + "m",
            "description:\n" + line_break(ship["description"], UI_FONT, self.info_box.surf.size[0] - 2 * self.info_box.text_pos[0])
        ]
    
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
        player.reverse_thruster_data = ship["reverse_thruster_data"]
        player.thruster_flame_image = self.thruster_images[ship["thruster_type"]]
    
    def set_location(self, image_loader, data):
        self.pos = pg.Vector2(data["pos"])
        self.size = pg.Vector2(data["size"])
        self.exit_pos = pg.Vector2(data["exit_pos"])

        image = pg.transform.scale(image_loader.stations[data["image_id"]], self.size)
        self.image_mosaic = ImageMosaic(image, data["mosaic_splitting"])