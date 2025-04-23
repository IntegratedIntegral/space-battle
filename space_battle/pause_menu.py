from settings import *
from button import Button
from info_panel import InfoPanel

class PauseMenu:
    def __init__(self):
        self.button_size = (150, 50)
        window_center_x = WINDOW_SEMI_WIDTH - self.button_size[0] / 2
        self.quit_button = Button((window_center_x, 600), self.button_size, "quit")
        self.key_bindings_button = Button((window_center_x, 530), self.button_size, "show key bindings")

        self.key_bindings_text_rows = [
            "pause: ESC",
            "accelerate: W",
            "deccelerate: S",
            "pull left: A",
            "pull right: D",
            "stability assist: SHIFT",
            "shoot: X",
            "toggle map: M",
            "dock: C",
            "center view: V",
            "pan view: LMB",
            "zoom: scroll",
            "map zoom: CTRL + scroll",
            "toggle locations menu: T",
            "toggle utility: G"
        ]
        #self.key_bindings_text_rows = self.key_bindings_text.split("\n")
        self.key_bindings_info_box = InfoPanel((1200, 265), (300, 400), text_pos=(30, 9), colour=BUTTON_COLOUR, text_colour=UI_TEXT_COLOUR, alpha=255)
        self.show_key_bindings = False
    
    def update(self, app):
        self.quit_button.update(app.window, app.lmb_pressed)
        self.key_bindings_button.update(app.window, app.lmb_pressed)

        if self.quit_button.pressed: app.running = False
        
        elif self.key_bindings_button.just_pressed: self.show_key_bindings = not self.show_key_bindings
        
        if self.show_key_bindings: self.key_bindings_info_box.base_draw(app.window, self.key_bindings_text_rows)