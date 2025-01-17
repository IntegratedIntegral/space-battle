from settings import *

class HealthUp():
    def __init__(self, image_loader, pos):
        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2(0)

        self.template_image = image_loader.HEALTH_UP_IMG

    def draw(self, window, camera):
        image = self.template_image

        size = camera.zoom * pg.Vector2(image.get_size())
        image = pg.transform.scale(image, size)

        rect = pg.Rect(0, 0, *image.get_size())
        rect.center = camera.screen_coords(self.pos.x, self.pos.y)

        window.blit(image, rect)
    
    def update(self, window, camera, player, battle_site, delta_t):
        self.draw(window, camera)
        self.update_pos(delta_t, battle_site)
        self.apply_health(delta_t, player, battle_site.hlthUps)
    
    def update_pos(self, delta_t, battle_site):
        self.pos += self.vel * delta_t #update pos of health up

        rel_pos = self.pos - battle_site.pos

        if rel_pos.magnitude_squared() >= BATTLE_SITE_RADIUS * BATTLE_SITE_RADIUS:
            self.pos.x -= 0.05 * rel_pos.x
            self.pos.y -= 0.05 * rel_pos.y
            self.vel.x = 0
            self.vel.y = 0
    
    def apply_health(self, delta_t, player, hlthUps):
        if player.health + HEALTH_BONUS <= player.max_health:
            rel_pos = player.pos - self.pos

            dist = rel_pos.magnitude()

            if dist <= PICK_UP_RADIUS: #player is within pickup range
                self.vel += (0.0004 * rel_pos / dist + 0.001 * (player.vel - self.vel)) * delta_t
                
                if player.pos.x > self.pos.x - 20 and player.pos.x < self.pos.x + 20 and player.pos.y > self.pos.y - 20 and player.pos.y < self.pos.y + 20: #player picked up health up
                    player.health += HEALTH_BONUS
                    hlthUps.remove(self)
    
    def show_info(self):
        return "health up"