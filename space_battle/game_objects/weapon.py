class Weapon:
    def __init__(self, name, damage, electronic_damage, speed, delay, dist, power_usage, mass, projectile_mass, sprite):
        self.name = name
        self.damage = damage
        self.electronic_damage = electronic_damage
        self.speed = speed
        self.delay = delay #delay (measured in milliseconds) between consecutive shots
        self.range = dist
        self.time = dist / speed #time (also in milliseconds) before projectile despawns
        self.power_usage = power_usage
        self.mass = mass #mass of weapon itself
        self.projectile_mass = projectile_mass #mass of projectile

        self.template_image = sprite