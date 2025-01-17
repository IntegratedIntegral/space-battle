from settings import *

class ImageMosaic: #a class used for splitting a large image into smaller parts so that only the parts that are visible will be blitted
    def __init__(self, image, splitting):
        self.splitting = splitting
        self.part_count = splitting[0] * splitting[1]
        self.part_size = (image.size[0] // splitting[0], image.size[1] // splitting[1])
        self.image_parts = self.generate_image_parts(image)
    
    def draw(self, window, pos, zoom):
        for i in range(self.part_count):
            x_i = i % self.splitting[0]
            y_i = i // self.splitting[0]
            x = zoom * x_i * self.part_size[0] + pos[0]
            y = zoom * y_i * self.part_size[1] + pos[1]

            apparent_size = (zoom * self.part_size[0], zoom * self.part_size[1])

            if x + apparent_size[0] > 0 and x < WINDOW_WIDTH and y + apparent_size[1] > 0 and y < WINDOW_HEIGHT: #image part is viewable inside the window
                image = pg.transform.scale(self.image_parts[i], apparent_size)
                window.blit(image, (x, y))
    
    def generate_image_parts(self, image):
        image_parts = []
        for i in range(self.part_count):
            x_i = i % self.splitting[0]
            y_i = i // self.splitting[0]
            x = x_i * self.part_size[0]
            y = y_i * self.part_size[1]

            surf = image.subsurface((x, y, self.part_size[0], self.part_size[1]))
            
            image_parts.append(surf)
        return image_parts