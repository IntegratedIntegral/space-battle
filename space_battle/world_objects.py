from settings import *
from game_objects.player import Player
from game_objects.battle_site import BattleSite
from game_objects.station import Station
from camera import Camera

class WorldObjects:
    def __init__(self, app, save_data, save_name):
        #collection of all objects in the world, including battle sites, player and stations
        self.app = app

        self.save_name = save_name

        self.active_location = app.locations[save_data["location_id"]]

        self.bg_image_id = self.active_location["bg_image"]

        self.camera = Camera()

        self.player = Player(save_data["pos"] if save_data["pos"] else self.active_location["start_pos"],
                             self.get_ship_type_by_name(save_data["ship_name"]),
                             self.get_weapon_type_by_name(save_data["weapon_name"]),
                             app.image_loader)

        self.battle_sites = self.generate_battle_sites(self.active_location["battle_sites"], save_data["battle_site_progress"][self.active_location["name"]])

        self.station = Station(self.active_location["station"], self.app.ship_types, self.app.weapon_types, app.image_loader)

        self.panning = False

        self.active_bs = None
    
    def generate_battle_sites(self, data, progress_data):
        battle_sites = []
        for i in range(len(data)):
            bs_data = data[i]
            complete = progress_data[i]
            battle_sites.append(BattleSite(self.app, bs_data["pos"], self.app.enemy_types, self.app.weapon_types, bs_data["difficulty"], bs_data["type"], complete))
        return battle_sites
    
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
        
        if not in_bs:
            self.active_bs = None

        #PLAYER
        if self.player.health > 0:
            self.player.update(self.app.window, self.app.key_state_pressed, self.app.key_state_just_pressed, self.camera, self.station, delta_t)
        
        elif self.player.explosion.time < EXPLOSION_TIME:
            self.player.explosion.explode(self.app.window, delta_t, self.camera)
        
        else: self.app.running = False
    
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
    
    def set_location(self, save_data, location):
        self.player.pos = pg.Vector2(location["start_pos"])
        self.player.vel = pg.Vector2()
        self.player.direction = 0
        self.player.angular_vel = 0

        self.station.set_location(self.app.image_loader, location["station"])

        self.app.save_data["battle_site_progress"][self.active_location["name"]] = self.get_bs_progress_for_active_location()

        self.battle_sites = self.generate_battle_sites(location["battle_sites"], save_data["battle_site_progress"][location["name"]])

        self.bg_image_id = location["bg_image"]
        self.active_location = location
    
    def get_ship_type_by_name(self, ship_name):
        for ship_type in self.app.ship_types:
            if ship_type["name"] == ship_name: return ship_type
    
    def get_weapon_type_by_name(self, weapon_name):
        for weapon_type in self.app.weapon_types:
            if weapon_type.name == weapon_name: return weapon_type
    
    def get_bs_progress_for_active_location(self):
        return [bs.complete for bs in self.battle_sites]
    
    def save(self):
        save_data = {
            "started": True,
            "location_id": self.app.locations.index(self.active_location),
            "ship_name": self.player.ship_type,
            "weapon_name": self.player.weapon.name,
            "pos": list(self.player.pos),
            "battle_site_progress": self.app.save_data["battle_site_progress"]
        }
        save_data["battle_site_progress"][self.active_location["name"]] = self.get_bs_progress_for_active_location()
        with open(join("save_data", self.save_name), "w") as file: json.dump(save_data, file)