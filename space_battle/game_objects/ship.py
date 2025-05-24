from settings import *
from game_objects.explosion import Explosion
from game_objects.projectile import Proj

class Ship:
    def __init__(self, pos, health, capacitor, charge_rate, thrust, angular_acc, weapon, mass, hitbox_semi_length, hitbox_semi_width, name, image_loader, thruster_data, thruster_type):
        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2(0)
        self.direction = 0
        self.angular_vel = 0
        self.angular_acc = pi / 180 * angular_acc #degrees / millisecond^2 -> radians / millisecond^2
        self.dir_vec = pg.Vector2(1.0, 0.0)

        self._weapon = weapon

        self._thrust = thrust
        self._hull_mass = mass #mass of ship without any weapons, utilities and upgrades
        self._mass = mass + weapon.mass
        self.acceleration = thrust / self._mass #in meters / millisecond^2
        self.health = health
        self.max_capacity = capacitor
        self.capacitor = capacitor
        self.charge_rate = charge_rate

        self.shoot_cool_down = 0
        
        self.projectiles = []

        self.stun_timer = 0

        self.explosion = Explosion(self, image_loader.EXPLOSION_PARTICLE_IMG)

        self.hitbox_semi_length = hitbox_semi_length
        self.hitbox_semi_width = hitbox_semi_width

        self.is_acc = False
        
        self.template_image = image_loader.ships[name]
        self.template_image = pg.transform.scale(self.template_image, (2 * hitbox_semi_length, 2 * hitbox_semi_width))
        self.thruster_flame_image = image_loader.thruster_flames[thruster_type]
        self.thruster_data = thruster_data

        self.ship_type = name
    
    def update_pos(self, delta_t):
        self.pos += self.vel * delta_t

        self.direction += self.angular_vel * delta_t
        self.dir_vec.x = cos(self.direction)
        self.dir_vec.y = sin(self.direction)

        #stop self from crossing border
        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x = 0
        elif self.pos.x > WORLD_SIZE:
            self.pos.x = WORLD_SIZE
            self.vel.x = 0
        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y = 0
        elif self.pos.y > WORLD_SIZE:
            self.pos.y = WORLD_SIZE
            self.vel.y = 0
    
    def update_timers(self, delta_t):
        if self.shoot_cool_down > 0: self.shoot_cool_down = max(self.shoot_cool_down - delta_t, 0)
        if self.stun_timer > 0: self.stun_timer = max(self.stun_timer - delta_t, 0)
    
    def recharge(self, delta_t):
        self.capacitor = min(self.max_capacity, self.capacitor + self.charge_rate * delta_t)
    
    def update_projectiles(self, window, delta_t, camera):
        for p in self.projectiles:
            p.draw(window, camera) #draw all projectiles
            p.update_pos(delta_t, self.projectiles)
    
    #ACTIONS
    def turn_right(self, delta_t):
        new_capacity = self.capacitor - TURN_POWER_USAGE * delta_t
        if new_capacity >= 0:
            self.angular_vel += self.angular_acc * delta_t #turn right
            self.capacitor = new_capacity
        else: self.stun_timer = STUN_DURATION

    def turn_left(self, delta_t):
        new_capacity = self.capacitor - TURN_POWER_USAGE * delta_t
        if new_capacity >= 0:
            self.angular_vel -= self.angular_acc * delta_t #turn left
            self.capacitor = new_capacity
        else: self.stun_timer = STUN_DURATION

    def acc(self, delta_t):
        new_capacity = self.capacitor - ACC_POWER_USAGE * delta_t
        if new_capacity >= 0:
            self.is_acc = True
            self.vel += self.acceleration * self.dir_vec * delta_t #accelerate
            self.capacitor = new_capacity
        else: self.stun_timer = STUN_DURATION
    
    def shoot(self):
        if self.shoot_cool_down == 0:
            if self.capacitor >= self._weapon.power_usage:
                self.projectiles.append(Proj(self)) #spawn projectile
                self.shoot_cool_down = self._weapon.delay
                self.capacitor -= self._weapon.power_usage

                #recoil
                self.vel -= self._weapon.speed * self._weapon.projectile_mass / self.mass * self.dir_vec
            else: self.stun_timer = STUN_DURATION

    def take_damage(self, weapon):
        self.health = max(self.health - weapon.damage, 0)
        self.capacitor = max(self.capacitor - weapon.electronic_damage, 0)
        if self.capacitor == 0: self.stun_timer = STUN_DURATION
    
    def draw(self, window, camera):
        image = self.template_image

        apparent_size = camera.zoom * pg.Vector2(image.get_size())
        image = pg.transform.scale(image, apparent_size)
        image = pg.transform.rotate(image, -180 / pi * self.direction)

        rect = pg.Rect(0, 0, *image.get_size())
        rect.center = camera.screen_coords(self.pos.x, self.pos.y)

        window.blit(image, rect)

        if self.is_acc: self.draw_thrust_flame(window, camera)
    
    def draw_thrust_flame(self, window, camera):  
        image = self.thruster_flame_image

        size = pg.Vector2(image.get_size())
        apparent_size = camera.zoom * size
        image = pg.transform.scale(image, apparent_size)
        image = pg.transform.rotate(image, -180 / pi * self.direction)

        rect = pg.Rect((0, 0), image.get_size())
        for flame_pos in self.thruster_data:
            pos = self.pos + (flame_pos[0] - size.x / 2) * self.dir_vec + flame_pos[1] * pg.Vector2(-self.dir_vec.y, self.dir_vec.x)
            rect.center = camera.screen_coords(pos.x, pos.y)

            window.blit(image, rect)
    
    def collision_detection(self, delta_t, attacker):
        for proj in attacker.projectiles:
            #defines coordinates in a coordinate system centered on ship and rotated such that the x axis is along the nose of the ship and the y
            #axis is towards the left of the ship
            relX = (proj.pos.x - self.pos.x) * self.dir_vec.x + (proj.pos.y - self.pos.y) * self.dir_vec.y
            relY = (self.pos.x - proj.pos.x) * self.dir_vec.y + (proj.pos.y - self.pos.y) * self.dir_vec.x
            prevX = relX + (self.vel.x - proj.vel.x) * delta_t
            prevY = relY + (self.vel.y - proj.vel.y) * delta_t

            hitBoxCorners = [
                [self.hitbox_semi_length * self.dir_vec.x - self.hitbox_semi_width * self.dir_vec.y, self.hitbox_semi_length * self.dir_vec.y + self.hitbox_semi_width * self.dir_vec.x],
                [-self.hitbox_semi_length * self.dir_vec.x - self.hitbox_semi_width * self.dir_vec.y, -self.hitbox_semi_length * self.dir_vec.y + self.hitbox_semi_width * self.dir_vec.x],
                [-self.hitbox_semi_length * self.dir_vec.x + self.hitbox_semi_width * self.dir_vec.y, -self.hitbox_semi_length * self.dir_vec.y - self.hitbox_semi_width * self.dir_vec.x],
                [self.hitbox_semi_length * self.dir_vec.x + self.hitbox_semi_width * self.dir_vec.y, self.hitbox_semi_length * self.dir_vec.y - self.hitbox_semi_width * self.dir_vec.x]
            ]
            for i in range(4):
                HBsegmentX = [hitBoxCorners[i][0], hitBoxCorners[(i + 1) % 4][0]]
                HBsegmentY = [hitBoxCorners[i][1], hitBoxCorners[(i + 1) % 4][1]]

                if (min(*HBsegmentX) < max(relX, prevX) and min(relX, prevX) < max(*HBsegmentX)) and (min(*HBsegmentY) < max(relY, prevY) and min(relY, prevY) < max(*HBsegmentY)): #when projectile hits ship health will decrease
                    self.take_damage(attacker.weapon)
                    attacker.projectiles.remove(proj)
                    return True
        return False
    
    @property
    def mass(self):
        return self._mass
    
    @mass.setter
    def mass(self, val):
        self._mass = val
        self.acceleration = self._thrust / self._mass #recalculate acceleration when mass is assigned a new value
    
    @property
    def hull_mass(self):
        return self._hull_mass
    
    @hull_mass.setter
    def hull_mass(self, val):
        self._hull_mass = val
        self.mass = self._hull_mass + self._weapon.mass #notice there is no _ before mass. this means mass.setter will be called so that the acceleration is recalculated
    
    @property
    def thrust(self):
        return self._thrust
    
    @thrust.setter
    def thrust(self, val):
        self._thrust = val
        self.acceleration = self._thrust / self._mass #recalculate acceleration when mass is assigned a new value
    
    @property
    def weapon(self):
        return self._weapon
    
    @weapon.setter
    def weapon(self, val):
        self._weapon = val
        self.mass = self._hull_mass + val.mass #notice there is no _ before mass. this means mass.setter will be called so that the acceleration is recalculated