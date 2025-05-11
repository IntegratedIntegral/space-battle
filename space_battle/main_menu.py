from settings import *
from button import Button

class MainMenu:
    def __init__(self):
        button_size = (150, 50)
        window_center_x = WINDOW_SEMI_WIDTH - button_size[0] // 2
        self.play_button = Button((window_center_x, 530), button_size, "play")
        self.quit_button = Button((window_center_x, 600), button_size, "quit")
    
    def update(self, app):
        self.play_button.update(app.window, app.lmb_pressed)
        self.quit_button.update(app.window, app.lmb_pressed)

        if self.play_button.pressed:
            pg.mouse.get_rel() #I don't really like this line. I added it because the camera would jump to some weird focus position when you pressed play
            app.mainmenu_active = False

        if self.quit_button.pressed: app.running = False