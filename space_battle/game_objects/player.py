from game_objects.ship import Ship
from settings import *
from info_panel import InfoPanel

class Player(Ship):
    def __init__(self, pos, start_ship, start_weapon, image_loader):
        super().__init__(pos, start_ship["health"], start_ship["capacitor"], start_ship["charge_rate"], start_ship["thrust"], start_ship["angular_acc"],
                         start_weapon,
                         start_ship["mass"], start_ship["dimensions"]["semi_length"], start_ship["dimensions"]["semi_width"], start_ship["name"], image_loader, start_ship["thruster_data"], start_ship["thruster_type"])
        self._utility = None

        self.max_health = start_ship["health"]
        self.reverse_thruster_data = start_ship["reverse_thruster_data"]
        self.is_decc = False

        self.is_mobile = True

        self.docked = False

        self.info_panel = InfoPanel((10, 735), (180, 185), text_pos=(10, 10))
    
    def update(self, window, key_state_pressed, key_state_just_pressed, camera, station, delta_t):
        if not self.docked:
            self.draw(window, camera)
            if self.is_decc: self.draw_reverse_thrust_flame(window, camera)
            self.is_acc = False
            self.is_decc = False
            self.update_pos(delta_t)
        
        self.recharge(delta_t)
        self.update_projectiles(window, delta_t, camera)
        self.update_timers(delta_t)

        if self.stun_timer == 0:
            self.peform_action(key_state_pressed, key_state_just_pressed, station, camera, delta_t)
            if self._utility: self._utility.update(self, delta_t)

    def decc(self, delta_t):
        new_capacity = self.capacitor - ACC_POWER_USAGE * delta_t
        if new_capacity >= 0:
            self.is_decc = True
            self.vel -= self.acceleration * self.dir_vec * delta_t #deccelerate
            self.capacitor = new_capacity
        else: self.stun_timer = STUN_DURATION
    
    def peform_action(self, key_state_pressed, key_state_just_pressed, station, camera, delta_t):
        #peform actions that are triggered by their coresponding flag variables
        if key_state_pressed[pg.K_d] and not self.docked and self.is_mobile:
            self.turn_right(delta_t) #turn right
        if key_state_pressed[pg.K_a] and not self.docked and self.is_mobile:
            self.turn_left(delta_t) #turn left
        if key_state_pressed[pg.K_w] and not self.docked and self.is_mobile:
            self.acc(delta_t) #accelerate
        if key_state_pressed[pg.K_s] and not self.docked and self.is_mobile:
            self.decc(delta_t) #deccelerate
        if key_state_pressed[pg.K_x] and not self.docked and self.is_mobile:
            self.shoot() #shoot
        if key_state_just_pressed[pg.K_c]:
            self.dock(station, camera)
        if key_state_pressed[pg.K_LSHIFT] and not self.docked and self.is_mobile:
            self.stability_assist(delta_t)
        if key_state_just_pressed[pg.K_g] and self._utility:
            self._utility.toggle(self)
    
    def draw_reverse_thrust_flame(self, window, camera):
        image = self.thruster_flame_image

        size = pg.Vector2(image.get_size())
        apparent_size = camera.zoom * size
        image = pg.transform.scale(image, apparent_size)
        image = pg.transform.rotate(image, 180 - 180 / pi * self.direction)

        rect = pg.Rect((0, 0), image.get_size())
        for flame_pos in self.reverse_thruster_data:
            pos = self.pos + (flame_pos[0] + size.x / 2) * self.dir_vec + flame_pos[1] * pg.Vector2(-self.dir_vec.y, self.dir_vec.x)
            rect.center = camera.screen_coords(pos.x, pos.y)

            window.blit(image, rect)
    
    def stability_assist(self, delta_t):
        sas_angular_acc = min(self.angular_acc, max(-self.angular_acc, self.angular_vel * SAS_DAMPENING))
        new_capacity = self.capacitor - abs(sas_angular_acc) / self.angular_acc * TURN_POWER_USAGE * delta_t
        if new_capacity >= 0:
            self.angular_vel -= sas_angular_acc * delta_t
            self.capacitor = new_capacity
    
    def dock(self, station, camera):
        #is the player within docking radius? if so, dock
        if (station.pos - self.pos).magnitude_squared() < DOCK_RADIUS * DOCK_RADIUS:
            self.docked = not self.docked
            self.vel.x = 0
            self.vel.y = 0
            self.pos = station.pos + station.exit_pos
            camera.zoom = 1.0
            camera.focus_pos = pg.Vector2()
    
    def show_info(self):
        return "you"
    
    @property
    def hull_mass(self):
        return self._hull_mass
    
    @hull_mass.setter
    def hull_mass(self, val):
        self._hull_mass = val
        if self._utility: self.mass = self._hull_mass + self._weapon.mass + self._utility.mass
        else: self.mass = self._hull_mass + self._weapon.mass
    
    @property
    def weapon(self):
        return self._weapon
    
    @weapon.setter
    def weapon(self, val):
        self._weapon = val
        if self._utility: self.mass = self._hull_mass + val.mass + self._utility.mass
        else: self.mass = self._hull_mass + val.mass

    @property
    def utility(self):
        return self._utility
    
    @utility.setter
    def utility(self, val):
        self._utility = val
        if val: self.mass = self._hull_mass + self._weapon.mass + val.mass
        else: self.mass = self._hull_mass + self._weapon.mass