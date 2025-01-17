from game_objects.ship import Ship
from random import randint
from settings import *
from ship_info_panel import ShipInfoPanel

class Enemy(Ship):
    def __init__(self, pos, health, capacitor, recharge_rate, acceleration, angular_acc, weapon, mass, hitbox_semi_length, hitbox_semi_width, ship_img_id, image_loader, thruster_data, thruster_type):
        super().__init__(pos, health, capacitor, recharge_rate, acceleration, angular_acc, weapon, mass, hitbox_semi_length, hitbox_semi_width, ship_img_id, image_loader, thruster_data, thruster_type)
        self.behaviour_timer = ENEMY_BEHAVIOUR_TIMER_DURATION
        self.phase_change = randint(ENEMY_BEHAVIOUR_TIMER_DURATION // 3, ENEMY_BEHAVIOUR_TIMER_DURATION * 2 // 3)
        self.ship_type = ship_img_id

        self.info_panel = ShipInfoPanel(self)
    
    @staticmethod
    def normalize_if_possible(vec):
        if vec.magnitude_squared():
            return vec.normalize()
        return pg.Vector2(0)
    
    def peform_action(self, player, battle_site, is_active, delta_t):
        rel_pos = battle_site.pos - self.pos
        if is_active and rel_pos.magnitude_squared() <= BATTLE_SITE_RADIUS * BATTLE_SITE_RADIUS:
            vec_to_player = player.pos - self.pos
            distance = vec_to_player.magnitude()
            future_pos = vec_to_player + (player.vel - self.vel) * vec_to_player.magnitude() / self.weapon.speed
            future_pos_norm = future_pos.normalize()
            cross_prod = -future_pos_norm.y * self.dir_vec.x + future_pos_norm.x * self.dir_vec.y

            if self.behaviour_timer > self.phase_change:
                cross_prod += ENEMY_SLOW_FACTOR * (self.vel.y * self.dir_vec.x - self.vel.x * self.dir_vec.y) #slow down if enemy is going too fast
                self.acc(delta_t) #acceleration phase
                self.is_acc = True
            
            elif cross_prod < COS_ENEMY_ALIGN_RANGE and distance <= self.weapon.range:
                self.shoot() #fighting phase

            if self.behaviour_timer > 0:
                self.behaviour_timer -= delta_t
            else:
                self.behaviour_timer = ENEMY_BEHAVIOUR_TIMER_DURATION
                self.phase_change = randint(ENEMY_BEHAVIOUR_TIMER_DURATION // 3, ENEMY_BEHAVIOUR_TIMER_DURATION * 2 // 3)
            
            target_pos = future_pos
        
        else: #outside of battle site! must return to battle site
            cross_prod = -rel_pos.y * self.dir_vec.x + rel_pos.x * self.dir_vec.y
            if rel_pos.normalize().dot(self.normalize_if_possible(self.vel)) < COS_ENEMY_ALIGN_RANGE or self.vel.magnitude() < ENEMY_RETURN_SPEED:
                self.acc(delta_t)
            
            target_pos = rel_pos
        
        target_dir = target_pos.normalize()
        slow_factor = (target_dir - self.dir_vec).magnitude() / 2 #a value that gets smaller as the enemy is more aligned to the target
        if cross_prod > 0: #must turn left
            if self.angular_vel > -ENEMY_ALIGN_RATE * slow_factor * (1 - ENEMY_ALIGN_ERROR_TOLERANCE): #increase angular speed
                self.turn_left(delta_t)
            elif self.angular_vel < -ENEMY_ALIGN_RATE * slow_factor * (1 + ENEMY_ALIGN_ERROR_TOLERANCE): #decrease angular speed
                self.turn_right(delta_t)
        else: #must turn right
            if self.angular_vel < ENEMY_ALIGN_RATE * slow_factor * (1 - ENEMY_ALIGN_ERROR_TOLERANCE): #increase angular speed
                self.turn_right(delta_t)
            elif self.angular_vel > ENEMY_ALIGN_RATE * slow_factor * (1 + ENEMY_ALIGN_ERROR_TOLERANCE): #decrease angular speed
                self.turn_left(delta_t)
    
    def update(self, window, camera, player, battle_site, is_active, delta_t):
        self.draw(window, camera)
        self.is_acc = False
        self.update_pos(delta_t)
        self.update_projectiles(window, delta_t, camera)
        self.recharge(delta_t)

        if player.health > 0:
            self.peform_action(player, battle_site, is_active, delta_t) #player is still alive! must hunt it down!
    
    def show_info(self):
        return self.ship_type + "\nhealth: " + str(self.health)