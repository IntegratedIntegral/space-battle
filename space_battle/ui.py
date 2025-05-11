from settings import *
from info_panel import InfoPanel

class UI:
    def __init__(self, player):
        self.player = player
        self.ene_info_panels = []
        self.player_info_panel = player.info_panel
        self.utility_panel = InfoPanel((200, 860), (80, 60), text_pos=(10, 5))
    
    def draw_direction_arrow(self, window):
        pg.draw.line(window, (43, 201, 212), self.player.dir_vec * 50 + self.center, self.player.dir_vec * 190 + self.center, width=2)
    
    def draw_ene_direction_arrows(self, window):
        for panel in self.ene_info_panels:
            ene = panel.ship
            vec_to_ene = ene.pos - self.player.pos
                
            arrow_dir = (vec_to_ene + (ene.vel - self.player.vel) * vec_to_ene.magnitude() / self.player.weapon.speed).normalize()
            pg.draw.line(window, (210, 210, 210), arrow_dir * 50 + self.center, arrow_dir * 240 + self.center, width=2)
    
    def draw(self, window, camera):
        #ARROWS
        if not self.player.docked:
            self.center = camera.screen_coords(self.player.pos.x, self.player.pos.y)
            self.draw_direction_arrow(window)
            self.draw_ene_direction_arrows(window)
        
        #INFO PANELS
        for info_panel in self.ene_info_panels:
            info_panel.draw(window, self.player)
        self.player_info_panel.base_draw(window, [
            f"health: {self.player.health}",
            f"capacitor: {round(self.player.capacitor)}MJ",
            f"acceleration: {round(self.player.acceleration * 1000000, 1)}m/s^2",
            f"speed: {round(self.player.vel.magnitude() * 1000)}m/s",
            "weapon: ",
            f"  damage: {self.player.weapon.damage}",
            f"  range: {self.player.weapon.range}m"
        ])

        #UTILITY PANEL
        if self.player.utility:
            self.utility_panel.base_draw(window, [
                self.player.utility.name,
                "active" if self.player.utility.active else "inactive"
            ])