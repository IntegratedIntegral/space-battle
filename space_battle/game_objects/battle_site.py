from game_objects.enemy import Enemy
from game_objects.health_up import HealthUp
from game_objects.asteroid import Asteroid
from game_objects.fire_work import FireWork
from settings import *
from random import random, randint


class BattleSite:
    def __init__(self, app, pos, enemy_types, weapon_types, difficulty, type, complete):
        self.app = app

        self.pos = pg.Vector2(pos)

        self.complete = complete

        self.difficulty = difficulty
        self.type = type

        self.asteroids = []
        self.spawn_asteroids()

        self.hlthUps = []

        self.enemies = []

        if not self.complete:
            self.get_ready_timer = GET_READY_DURATION

            self.fire_works = [
                FireWork(),
                FireWork(),
                FireWork()
            ]
            self.fire_work_time = 0

            self.enemy_waves = self.generate_enemy_waves(weapon_types)
            self.enemy_types = enemy_types
            self.level = 0
    
    def generate_enemy_waves(self, weapon_types):
        enemy_count = BATTLE_SITE_WAVE_SIZE[self.difficulty]
        
        waves = []
        ship_options = BATTLE_SITE_ENEMY_SHIP_TYPES[self.type]
        weapon_options = BATTLE_SITE_ENEMY_WEAPON_TYPES[self.type]
        
        for _ in range(3): #loop over the three waves
            wave = []
            for e in range(enemy_count): #loop over each enemy of the wave
                ene_type = ship_options[randint(0, len(ship_options) - 1)]
                ene_weapon_name = weapon_options[randint(0, len(weapon_options) - 1)]
                for weapon in weapon_types:
                    if weapon.name == ene_weapon_name:
                        ene_weapon = weapon
                        break

                wave.append((ene_type, ene_weapon, BATTLE_SITE_RADIUS * (2 * random() - 1), BATTLE_SITE_RADIUS * (2 * random() - 1)))
            
            waves.append(wave)
        
        return waves
    
    def spawn_enemies(self):
        wave = self.enemy_waves[self.level]
        for e in range(len(wave)):
            ene = wave[e]
            pos = pg.Vector2(ene[2], ene[3]) + self.pos

            for ene_type_candidate in self.enemy_types:
                if ene_type_candidate["name"] == ene[0]:
                    ene_type = ene_type_candidate
                    break
            
            self.enemies.append(Enemy(pos, ene_type["health"], ene_type["capacitor"], ene_type["charge_rate"], ene_type["thrust"], ene_type["angular_acc"],
                                      ene[1], #weapon
                                      ene_type["mass"], ene_type["dimensions"]["semi_length"], ene_type["dimensions"]["semi_width"],
                                      ene_type["name"], self.app.image_loader, ene_type["thruster_data"], ene_type["thruster_type"]))
            
            self.enemies[e].info_panel.pos = (480 + 200 * e, 35)
            self.app.ui.ene_info_panels.append(self.enemies[e].info_panel)

        self.level += 1
    
    def check_end(self, delta_t, is_active):
        if self.get_ready_timer == 0: #if enemies are defeated proceed to next level
            if self.level == len(self.enemy_waves): #all levels completed! set off the fireworks!
                if self.fire_work_time < 2400:
                    #FIREWORKS
                    for fw in self.fire_works:
                        fw.draw(self.app.window, self.fire_work_time)
                    self.fire_work_time += delta_t

                else:
                    self.complete = True #all enemies defeated! battle site complete
            else: #move on to next level
                self.spawn_enemies()
                self.get_ready_timer = GET_READY_DURATION
        
        elif len(self.enemies) == 0 and is_active:
            #draw timer bar
            pg.draw.rect(self.app.window, (214, 214, 105), pg.Rect(
                (WINDOW_WIDTH - 0.033 * GET_READY_DURATION)/2, 10,
                0.033 * self.get_ready_timer, 25
            ))

            self.get_ready_timer = max(self.get_ready_timer - delta_t, 0)
    
    @staticmethod
    def asteroid_size(t):
        return (MAX_ASTEROID_RADIUS - MIN_ASTEROID_RADIUS) / 2 * t * (t * t * t * t * t + 1) + MIN_ASTEROID_RADIUS
    
    def spawn_asteroids(self):
        for _ in range(30):
            r = random() ** 0.5 * BATTLE_SITE_RADIUS
            a = random() * 2 * pi
            x = r * cos(a) + self.pos.x
            y = r * sin(a) + self.pos.y
            self.asteroids.append(Asteroid(self.app.image_loader, (x, y), self.asteroid_size(random())))
    
    def update_enemies(self, delta_t, player, camera, is_active):
        for ene in self.enemies:
            if ene.health > 0:
                ene.update(self.app.window, camera, player, self, is_active, delta_t)

                if (player.pos - self.pos).magnitude_squared() <= BATTLE_SITE_RADIUS * BATTLE_SITE_RADIUS:
                    collided = ene.collision_detection(delta_t, player) #when player hits enemy enemie's health will decrease

                    if collided and ene.health == 0: self.hlthUps.append(HealthUp(self.app.image_loader, ene.pos)) #enemy ship destroyed! spawns a health up
                
            elif ene.explosion.time < EXPLOSION_TIME: ene.explosion.explode(self.app.window, delta_t, camera) #enemy ship destroyed! spawns smoke particles
            
            else:
                self.app.ui.ene_info_panels.remove(ene.info_panel)
                self.enemies.remove(ene)
            
            player.collision_detection(delta_t, ene) #when enemy hits player health will decrease
    
    def update(self, delta_t, player, camera, is_active):
        #HEALTH UPS
        for h in self.hlthUps:
            h.update(self.app.window, camera, player, self, delta_t)
        
        #ASTEROIDS
        for a in self.asteroids:
            a.update(self.app.window, camera, self.enemies + [player], self, delta_t)
        
        if not self.complete:
            #ENEMIES
            self.update_enemies(delta_t, player, camera, is_active)
            
            self.check_end(delta_t, is_active)
    
    def show_info(self):
        return "battle site." + (" (complete)" if self.complete else "") + "\ndifficulty: " + self.difficulty + "\ntype: " + self.type