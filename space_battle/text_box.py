from settings import *

class TextBox:
    def __init__(self, pos, size, text, colour=BUTTON_COLOUR, text_colour=UI_TEXT_COLOUR):
        self.surf = pg.surface.Surface(size)
        self.surf.fill(colour)
        text_surf = UI_FONT.render(text, True, text_colour, bgcolor=colour)
        self.surf.blit(text_surf, ((size[0] - text_surf.size[0]) // 2, (size[1] - text_surf.size[1]) // 2))

        self.pos = pos
    
    def draw(self, window):
        window.blit(self.surf, self.pos)