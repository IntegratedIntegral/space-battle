from game_objects.ship import Ship
from settings import *
from info_panel import InfoPanel

class Player(Ship):
    def __init__(self, pos, start_ship, start_weapon, image_loader):
        super().__init__(pos, start_ship["health"], start_ship["capacitor"], start_ship["charge_rate"], start_ship["acceleration"], start_ship["angular_acc"],
                         start_weapon,
                         start_ship["mass"], start_ship["dimensions"]["semi_length"], start_ship["dimensions"]["semi_width"], start_ship["name"], image_loader, start_ship["thruster_data"], start_ship["thruster_type"])
        self.max_health = start_ship["health"]

        self.acc_key = False
        self.decc_key = False
        self.turn_left_key = False
        self.turn_right_key = False
        self.shoot_key = False
        self.SAS = False

        self.docked = False

        self.info_panel = InfoPanel((180, 180))
        self.info_panel.pos = (10, 740)

    def decc(self, delta_t):
        new_capacity = self.capacitor - ACC_POWER_USAGE * delta_t
        if new_capacity >= 0:
            self.vel -= self.acceleration * pg.Vector2(cos(self.direction), sin(self.direction)) * delta_t #deccelerate
            self.capacitor = new_capacity
    
    def stability_assist(self, delta_t):
        sas_angular_acc = min(self.angular_acc, max(-self.angular_acc, self.angular_vel * SAS_DAMPENING))
        new_capacity = self.capacitor - abs(sas_angular_acc) / self.angular_acc * TURN_POWER_USAGE * delta_t
        if new_capacity >= 0:
            self.angular_vel -= sas_angular_acc * delta_t
            self.capacitor = new_capacity
    
    def peform_action(self, key_state_pressed, key_state_just_pressed, station, camera, delta_t):
        #peform actions that are triggered by their coresponding flag variables
        if key_state_pressed[pg.K_d] and not self.docked:
            self.turn_right(delta_t) #turn right
        if key_state_pressed[pg.K_a] and not self.docked:
            self.turn_left(delta_t) #turn left
        if key_state_pressed[pg.K_w] and not self.docked:
            self.acc(delta_t) #accelerate
        if key_state_pressed[pg.K_s] and not self.docked:
            self.decc(delta_t) #deccelerate
        if key_state_pressed[pg.K_x] and not self.docked:
            self.shoot() #shoot
        if key_state_just_pressed[pg.K_c]:
            self.dock(station, camera)
        if key_state_pressed[pg.K_LSHIFT]:
            self.stability_assist(delta_t)
    
    def draw_arrow(self, window, camera, battle_site):
        center = camera.screen_coords(self.pos.x, self.pos.y)
        if battle_site:
            #draws lines that act as guides for which direction to shoot. Takes into account the motion of the player and the enemy
            for ene in battle_site.enemies:
                vec_to_ene = ene.pos - self.pos
            
                arrow_dir = (vec_to_ene + (ene.vel - self.vel) * vec_to_ene.magnitude() / self.weapon.speed).normalize()
                pg.draw.line(window, (210, 210, 210), arrow_dir * 50 + center, arrow_dir * 240 + center, width=2)
    
    def dock(self, station, camera):
        #is the player within docking radius? if so, dock
        if (station.pos - self.pos).magnitude_squared() < DOCK_RADIUS * DOCK_RADIUS:
            self.docked = not self.docked
            self.vel.x = 0
            self.vel.y = 0
            self.pos = station.pos + station.exit_pos
            camera.zoom = 1.0
            camera.focus_pos = pg.Vector2()

    def update(self, window, key_state_pressed, key_state_just_pressed, camera, station, delta_t):
        if not self.docked:
            self.draw(window, camera)
            self.is_acc = False
            self.update_pos(delta_t)
        
        self.recharge(delta_t)
        self.update_projectiles(window, delta_t, camera)
        self.peform_action(key_state_pressed, key_state_just_pressed, station, camera, delta_t)
        
    
    def show_info(self):
        return "you"