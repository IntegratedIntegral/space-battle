class Weapon:
    def __init__(self, name, damage, speed, delay, dist, power_usage, sprite):
        self.name = name
        self.damage = damage
        self.speed = speed
        self.delay = delay #delay (measured in milliseconds) between consecutive shots
        self.range = dist
        self.time = dist / speed #time (also in milliseconds) before projectile despawns
        self.power_usage = power_usage

        self.template_image = sprite