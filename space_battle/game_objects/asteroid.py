from settings import *
from random import random

class Asteroid:
    def __init__(self, image_loader, pos, radius):
        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2(0)
        self.radius = radius
        self.mass = ASTEROID_DENSITY * pi * self.radius * self.radius

        self.template_image = image_loader.ASTEROID_1_IMG if random() < 0.5 else image_loader.ASTEROID_2_IMG
        
        self.template_image = pg.transform.scale(self.template_image, (2 * self.radius, 2 * self.radius))

        ran_angle = random() * 360
        self.template_image = pg.transform.rotate(self.template_image, ran_angle) #rotates asteroid to give the illusion of uniqueness
    
    def update(self, window, camera, ships, battle_site, delta_t):
        self.draw(window, camera)
        self.update_pos(battle_site, delta_t)
        for ship in ships:
            self.collision_detection(ship)
    
    def update_pos(self, battle_site, delta_t):
        self.pos += self.vel * delta_t

        rel_pos = self.pos - battle_site.pos

        if rel_pos.magnitude_squared() >= BATTLE_SITE_RADIUS * BATTLE_SITE_RADIUS:
            self.pos -= 1.99 * rel_pos
    
    def draw(self, window, camera):
        screen_pos = camera.screen_coords(self.pos.x, self.pos.y)
        apparent_radius = camera.zoom * self.radius

        if screen_pos[0] > -apparent_radius and screen_pos[0] < WINDOW_WIDTH + apparent_radius and screen_pos[1] > -apparent_radius and screen_pos[1] < WINDOW_HEIGHT + apparent_radius:
            image = self.template_image

            size = camera.zoom * pg.Vector2(image.get_size())
            image = pg.transform.scale(image, size)

            rect = pg.Rect(0, 0, *image.get_size())
            rect.center = screen_pos

            window.blit(image, rect)
    
    def collision_detection(self, ship):
        for proj in ship.projectiles:
            rel_pos = proj.pos - self.pos
            rel_vel = proj.vel - self.vel
            
            if rel_pos.magnitude_squared() <= self.radius * self.radius: #has the projectile touched the asteroid?
                self.vel += rel_vel * proj.weapon.mass / self.mass
                
                ship.projectiles.remove(proj)
        
        rel_pos = ship.pos - self.pos
        rel_vel = ship.vel - self.vel

        dist = rel_pos.magnitude()

        if dist <= self.radius: #has ship touched asteroid?
            unit_norm = rel_pos.x / dist
            unit_tang = rel_pos.y / dist

            ship_vel_norm = ship.vel.x * unit_norm + ship.vel.y * unit_tang
            ship_vel_tang = -ship.vel.x * unit_tang + ship.vel.y * unit_norm
            ast_vel_norm = self.vel.x * unit_norm + self.vel.y * unit_tang
            ast_vel_tang = -self.vel.x * unit_tang + self.vel.y * unit_norm

            new_ship_vel_norm = ((ship.mass - self.mass) * ship_vel_norm + 2 * ast_vel_norm * self.mass) / (self.mass + ship.mass)
            new_ast_vel_norm = ((self.mass - ship.mass) * ast_vel_norm + 2 * ship_vel_norm * ship.mass) / (ship.mass + self.mass)

            ship.vel.x = new_ship_vel_norm * unit_norm - ship_vel_tang * unit_tang
            ship.vel.y = new_ship_vel_norm * unit_tang + ship_vel_tang * unit_norm
            self.vel.x = new_ast_vel_norm * unit_norm - ast_vel_tang * unit_tang
            self.vel.y = new_ast_vel_norm * unit_tang + ast_vel_tang * unit_norm

            ship.pos = self.pos + self.radius / dist * rel_pos #puts ship on the edge of asteroid incase the ship plunged too deeply into the asteroid