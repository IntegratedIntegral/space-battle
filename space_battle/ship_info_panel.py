from info_panel import InfoPanel

class ShipInfoPanel(InfoPanel):
    def __init__(self, ship):
        super().__init__((180, 180))
        self.ship = ship
    
    def draw(self, window, player):
        self.base_draw(window, [
            self.ship.ship_type,
            f"health: {self.ship.health}",
            f"capacitor: {int(self.ship.capacitor)}MJ",
            f"distance: {int((self.ship.pos - player.pos).magnitude())}m",
            f"speed: {int(self.ship.vel.magnitude() * 1000)}m/s",
            f"relative speed: {int((self.ship.vel - player.vel).magnitude() * 1000)}m/s",
        ])