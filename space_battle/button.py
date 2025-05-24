from settings import *

class Button:
    def __init__(self, pos, size, text, colour=BUTTON_COLOUR):
        self.rect = pg.Rect(pos, size)
        self.colour = colour
        
        self.surf = pg.surface.Surface(self.rect.size)
        self.get_text_surf(text)

        self.pressed = False
        self.just_pressed = False
        self.hovered = False
    
    def get_text_surf(self, text):
        self.surf.fill(self.colour)
        text_surf = UI_FONT.render(text, True, UI_TEXT_COLOUR, bgcolor=self.colour)
        self.surf.blit(text_surf, ((self.rect.width - text_surf.size[0]) // 2, (self.rect.height - text_surf.size[1]) // 2))
    
    def update(self, window, lmb_pressed):
        window.blit(self.surf, self.rect)

        old_pressed = self.pressed
        old_hovered = self.hovered
        mouse_pos = pg.mouse.get_pos()
        
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.pressed = lmb_pressed and self.hovered
        self.just_pressed = not old_pressed and old_hovered and self.pressed