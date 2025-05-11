import json
from game_objects.player import Player
from game_objects.battle_site import BattleSite
from game_objects.station import Station
from game_objects.weapon import Weapon
from settings import *
from camera import Camera

class WorldObjects:
    def __init__(self, app, location):
        #collection of all objects in the world, including battle sites, player and stations
        self.app = app

        self.active_location_name = location["name"]

        self.bg_image_id = location["bg_image"]

        self.camera = Camera()

        self.ships = self.load_ships()
        self.weapons = self.load_weapons(app.image_loader.projectiles)
        self.enemy_types = self.load_enemies()

        self.player = Player(location["start_pos"], self.ships[0], self.weapons[0], app.image_loader)

        self.battle_sites = self.generate_battle_sites(location["battle_sites"])

        self.station = Station(location["station"], self.ships, self.weapons, app.image_loader)

        self.panning = False

        self.active_bs = None
    
    def generate_battle_sites(self, data):
        battle_sites = []
        for bs_data in data:
            battle_sites.append(BattleSite(self.app, bs_data["pos"], self.enemy_types, self.weapons, bs_data["difficulty"], bs_data["type"]))
        return battle_sites
    
    @staticmethod
    def load_ships():
        with open("game_objects/ship_types.json") as file:
            data = json.load(file)
        return data
    
    @staticmethod
    def load_enemies():
        with open("game_objects/enemy_types.json") as file:
            data = json.load(file)
        return data

    @staticmethod
    def load_weapons(images):
        weapons = []
        with open("game_objects/weapon_types.json") as file:
            data = json.load(file)
            for w in data:
                weapons.append(Weapon(w["name"], w["damage"], w["electronic_damage"], w["speed"], w["delay"], w["range"], w["power_usage"], w["mass"], w["projectile_mass"], images[w["image_id"]]))
        return weapons
    
    def update(self, delta_t):
        self.camera_control()

        #STATION
        self.station.draw(self.app.window, self.camera)

        #BATTLE SITES
        in_bs = False
        for bs in self.battle_sites:
            rel_pos = self.player.pos - bs.pos
            dist_sqrd = rel_pos.magnitude_squared()
            if dist_sqrd < 4 * BATTLE_SITE_RADIUS * BATTLE_SITE_RADIUS:
                bs.update(delta_t, self.player, self.camera, dist_sqrd <= BATTLE_SITE_RADIUS * BATTLE_SITE_RADIUS)
                self.active_bs = bs
                in_bs = True
            elif bs.complete:
                #remove battle site if it has been completed
                self.battle_sites.remove(bs)
        
        if not in_bs:
            self.active_bs = None

        #PLAYER
        if self.player.health > 0:
            self.player.update(self.app.window, self.app.key_state_pressed, self.app.key_state_just_pressed, self.camera, self.station, delta_t)
        
        elif self.player.explosion.time < EXPLOSION_TIME:
            self.player.explosion.explode(self.app.window, delta_t, self.camera)
        
        else:
            self.app.running = False
    
    def camera_control(self):
        if not self.player.docked:
            if self.app.scroll_forward and not self.app.key_state_pressed[pg.K_LCTRL]:
                self.camera.zoom_in()
            elif self.app.scroll_back and not self.app.key_state_pressed[pg.K_LCTRL]:
                self.camera.zoom_out()
        
        self.panning = self.app.lmb_pressed
        
        if self.player.docked:
            #focus on station when docked to it
            self.camera.focus(self.station.pos)
        else:
            #otherwise focus on player
            self.camera.focus(self.player.pos)
        
        rel = pg.Vector2(pg.mouse.get_rel())
        if self.panning:
            self.camera.update_offset(rel)
        
        if self.app.key_state_just_pressed[pg.K_v]:
            self.camera.offset.x, self.camera.offset.y = 0, 0 #center view
    
    def set_location(self, location):
        self.player.pos = pg.Vector2(location["start_pos"])
        self.player.vel = pg.Vector2()
        self.player.direction = 0
        self.player.angular_vel = 0

        self.station.set_location(self.app.image_loader, location["station"])

        self.battle_sites = self.generate_battle_sites(location["battle_sites"])

        self.bg_image_id = location["bg_image"]
        self.active_location_name = location["name"]