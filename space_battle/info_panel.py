from settings import pg

class InfoPanel:
    def __init__(self, size):
        self.colour = (82, 89, 122)
        self.surf = pg.surface.Surface((size))
        self.surf.set_alpha(192)
        self.pos = None

        self.font = pg.font.SysFont("Arial", 12)
    
    def render_text(self, text, pos):
        text_surf = self.font.render(text, False, (255, 255, 255))
        self.surf.blit(text_surf, pos)
    
    def base_draw(self, window, rows):
        self.surf.fill(self.colour)

        for i in range(len(rows)):
            row = rows[i]
            self.render_text(row, (10, 20 + 25 * i))

        window.blit(self.surf, self.pos)