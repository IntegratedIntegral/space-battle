from settings import pg, join, WINDOW_WIDTH, WINDOW_HEIGHT

class ImageLoader:
    def __init__(self):
        #asteroids
        self.ASTEROID_1_IMG = self.load_image("asteroids", "small_asteroid")
        self.ASTEROID_2_IMG = self.load_image("asteroids", "medium_asteroid")

        #projectiles
        self.projectiles = {
            "proj_1": self.load_image("projectiles", "proj_1"),
            "proj_2": self.load_image("projectiles", "proj_2"),
            "proj_3": self.load_image("projectiles", "proj_3"),
            "proj_5": self.load_image("projectiles", "proj_5"),
            "soldier_proj": self.load_image("projectiles", "soldier_proj"),
            "zoomer_proj": self.load_image("projectiles", "zoomer_proj"),
            "bomber_proj": self.load_image("projectiles", "bomber_proj"),
            "mothership_proj": self.load_image("projectiles", "mothership_proj")
        }

        #ships
        self.ships = {
            "sunspot": self.load_image("ships", "player"),
            "boulder": self.load_image("ships", "player_heavy"),
            "mayfly": self.load_image("ships", "player_light"),
            "soldier": self.load_image("ships", "soldier"),
            "zoomer": self.load_image("ships", "zoomer"),
            "bomber": self.load_image("ships", "bomber"),
            "mothership": self.load_image("ships", "mothership")
        }

        #stations
        self.stations = {
            "earth_station": self.load_image("stations", "earth_station"),
            "moon_station": self.load_image("stations", "moon_station")
        }

        #healthup
        self.HEALTH_UP_IMG = self.load_image("health_up")

        #thruster flame
        self.thruster_flames = [
            self.load_image("effects", "thruster_flame"),
            self.load_image("effects", "thruster_flame1")
        ]
        self.EXPLOSION_PARTICLE_IMG = self.load_image("effects", "explosion_particle")

        #bg images
        self.bg_images = {
            "earth_bg_new": self.load_bg("earth_bg_new"),
            "moon_bg": self.load_bg("moon_bg"),
            "mars_bg": self.load_bg("mars_bg")
        }

    @staticmethod
    def load_image(*path):
        path_png = list(path)
        path_png[len(path_png) - 1] += ".png" #add .png to the last element

        image = pg.image.load(join("assets", *path_png)).convert()
        image.set_colorkey((0, 0, 0))
        return image
    
    @staticmethod
    def load_bg(*path):
        path_png = list(path)
        path_png[len(path_png) - 1] += ".png" #add .png to the last element

        image = pg.image.load(join("assets", "backgrounds", *path_png)).convert()
        image = pg.transform.scale(image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        return image