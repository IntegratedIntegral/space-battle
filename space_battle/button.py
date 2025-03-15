from settings import *

class Button:
    def __init__(self, pos, size, text, colour=BUTTON_COLOUR):
        self.rect = pg.Rect(pos, size)
        
        self.surf = pg.surface.Surface(size)
        self.surf.fill(colour)
        text_surf = UI_FONT.render(text, True, UI_TEXT_COLOUR, bgcolor=colour)
        self.surf.blit(text_surf, ((size[0] - text_surf.size[0]) // 2, (size[1] - text_surf.size[1]) // 2))

        self.pressed = False
        self.just_pressed = False
        self.hovered = False
    
    def update(self, window, lmb_pressed):
        window.blit(self.surf, self.rect)

        old_pressed = self.pressed
        mouse_pos = pg.mouse.get_pos()
        
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.pressed = lmb_pressed and self.hovered
        self.just_pressed = not old_pressed and self.pressed