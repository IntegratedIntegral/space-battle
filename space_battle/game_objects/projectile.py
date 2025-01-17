from settings import *

class Proj():
    def __init__(self, ship):
        self.pos = ship.pos
        self.direction = ship.direction
        self.vel = ship.weapon.speed * ship.dir_vec + ship.vel
        self.weapon = ship.weapon
        self.time = self.weapon.time
    
    def draw(self, window, camera):
        image = self.weapon.template_image

        size = camera.zoom * pg.Vector2(image.get_size())
        image = pg.transform.scale(image, size)
        image = pg.transform.rotate(image, -180 / pi * self.direction)

        rect = pg.Rect(0, 0, *image.get_size())
        rect.center = camera.screen_coords(self.pos.x, self.pos.y)

        window.blit(image, rect)
    
    def update_pos(self, delta_t, projectiles):
        if self.time <= 0: #gets deleted if time runs out
            projectiles.remove(self)
        
        self.pos = self.pos + self.vel * delta_t #update pos of projectile
        self.time -= delta_t