from random import random, randint
from settings import *

class FireWork():
    def __init__(self):
        self.x = randint(154, WINDOW_WIDTH - 154)
        self.y = randint(154, WINDOW_HEIGHT - 154)
        self.colour = [randint(0, 255), randint(0, 255), randint(0, 255)]
        self.rays = randint(3, 10)
        self.spiralness = random()*0.785398163397448
    
    def draw(self, window, fire_work_time):
        for i in range(min(int(fire_work_time * 0.013333333333333), 8)):
            brightness = (i + 1)/(fire_work_time * 0.013333333333333)
            colour = (self.colour[0]*brightness, self.colour[1]*brightness, self.colour[2]*brightness)
            for r in range(self.rays):
                relX = 16*(i + 1)*cos(6.283185307179586/self.rays*r + self.spiralness*i)
                relY = 16*(i + 1)*sin(6.283185307179586/self.rays*r + self.spiralness*i)
                
                pg.draw.polygon(window, colour, (
                    (relX + self.x + 2 + i, relY + self.y),
                    (relX + self.x, relY + self.y + 2 + i),
                    (relX + self.x - 2 - i, relY + self.y),
                    (relX + self.x, relY + self.y - 2 - i)
                ))