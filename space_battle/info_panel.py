from settings import *

class InfoPanel:
    def __init__(self, pos, size, text_pos=(10, 20), colour=(82, 89, 122), text_colour=(255, 255, 255), alpha=192):
        self.text_pos = text_pos
        self.colour = colour
        self.text_colour = text_colour
        self.surf = pg.surface.Surface((size))
        if alpha != 255: self.surf.set_alpha(alpha)
        self.pos = pos

        #self.font = pg.font.SysFont("Arial", 12)
    
    def render_text(self, text, pos):
        text_surf = UI_FONT.render(text, True, self.text_colour, bgcolor=self.colour)
        self.surf.blit(text_surf, pos)
    
    def base_draw(self, window, rows):
        self.surf.fill(self.colour)

        for i in range(len(rows)):
            row = rows[i]
            self.render_text(row, (self.text_pos[0], self.text_pos[1] + 25 * i))

        window.blit(self.surf, self.pos)