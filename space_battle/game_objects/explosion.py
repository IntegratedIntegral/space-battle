from random import randint, random
from settings import *

class Explosion():
    def __init__(self, ship, image):
        self.clouds = 80
        self.speeds = []
        self.sizes = []
        for _ in range(self.clouds):
            self.speeds.append(random() * 0.4 + 0.1) #randoms values between 0.1 and 0.5
            self.sizes.append(randint(7, 14))
        
        self.time = 0
        
        self.ship = ship

        self.image = image
    
    def explode(self, window, delta_t, camera):
        for i in range(self.clouds):
            x = cos(2 * pi / self.clouds * i) * self.speeds[i] * self.time + self.ship.pos.x
            y = sin(2 * pi / self.clouds * i) * self.speeds[i] * self.time + self.ship.pos.y
            
            apparent_size = camera.zoom * self.sizes[i]
            image = pg.transform.scale(self.image, (apparent_size, apparent_size))
            rect = pg.Rect(camera.screen_coords(x - apparent_size / 2, y - apparent_size / 2), (apparent_size, apparent_size))
            window.blit(image, rect)
        
        self.time += delta_t