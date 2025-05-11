from settings import *

class Utility:
    def __init__(self, name, mass, player_imobile_during_operation):
        self.active = False
        self.name = name
        self.mass = mass
        self.player_imobile_during_operation = player_imobile_during_operation
    
    def toggle(self, player):
        self.active = not self.active
        player.is_mobile = not (self.active and self.player_imobile_during_operation)

class Repairer(Utility):
    def __init__(self):
        super().__init__("repairer", 6.3, True)
        self.repair_amount = 1
        self.interval = 4500
        self.capacitor_usage = 22.0
        self.timer = self.interval

        self.info_rows = [ #info to be displayed when in station
            "Slowly repairs the ship while active",
            "Ship is imobile while active",
            f"repair amount: {self.repair_amount}",
            f"repair interval: {self.interval / 1000}s",
            f"capacitor usage: {self.capacitor_usage}MJ",
            f"mass: {self.mass}tonnes",
            f"wattage: {round(self.capacitor_usage / self.interval * 1000, 3)}MW"
        ]
    
    def update(self, player, delta_t):
        if self.active:
            new_timer = (self.timer - delta_t) % self.interval
            if new_timer > self.timer:
                player.health = min(player.health + self.repair_amount, player.max_health)
                if player.health == player.max_health:
                    self.active = False
                    player.is_mobile = True
                new_capacity = player.capacitor - self.capacitor_usage
                if new_capacity >= 0:
                    player.capacitor = new_capacity
                else:
                    player.stun_timer = STUN_DURATION
                    self.active = False
            self.timer = new_timer