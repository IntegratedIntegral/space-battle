import pygame as pg
import json
from os.path import join
from math import *

pg.font.init()

WINDOW_WIDTH = 1700
WINDOW_HEIGHT = 930
WINDOW_SEMI_WIDTH = WINDOW_WIDTH // 2
WINDOW_SEMI_HEIGHT = WINDOW_HEIGHT // 2

UI_FONT = pg.font.SysFont("arial", 14)
BUTTON_COLOUR = (43, 201, 212)
UI_TEXT_COLOUR = (7, 62, 82)

WORLD_SIZE = 64000
BATTLE_SITE_RADIUS = 5000

ZOOM_RATE = 1.04
MIN_ZOOM = 0.4
MAX_ZOOM = 3.5

DOCK_RADIUS = 1500

PICK_UP_RADIUS = 650
SAS_DAMPENING = 0.011

ENEMY_ALIGN_RATE = 0.00314159265359
ENEMY_BEHAVIOUR_TIMER_DURATION = 10800
ENEMY_SLOW_FACTOR = 5
ENEMY_ALIGN_ERROR_TOLERANCE = 0.06
ENEMY_RETURN_SPEED = 0.12
COS_ENEMY_ALIGN_RANGE = cos(pi / 6)

ACC_POWER_USAGE = 0.033
TURN_POWER_USAGE = 0.004
STUN_DURATION = 5000

HEALTH_BONUS = 9

GET_READY_DURATION = 12000
EXPLOSION_TIME = 1500

BATTLE_SITE_WAVE_SIZE = {
    "easy": 2,
    "medium": 3,
    "hard": 4
}
BATTLE_SITE_ENEMY_SHIP_TYPES = {
    "explosives test site": ["soldier", "bomber"],
    "lightweight fleet": ["soldier", "zoomer"],
    "heavily armoured fleet": ["bomber", "mothership"]
}
BATTLE_SITE_ENEMY_WEAPON_TYPES = {
    "explosives test site": ["explosive launcher type A", "explosive launcher type B"],
    "lightweight fleet": ["radioactive A", "plasma short-range", "plasma mid-range"],
    "heavily armoured fleet": ["explosive launcher type A", "radioactive B", "plasma short-range", "kinetic railgun"]
}

MIN_ASTEROID_RADIUS = 20
MAX_ASTEROID_RADIUS = 400
ASTEROID_COLOUR = (89, 71, 60)
ASTEROID_DENSITY = 0.008