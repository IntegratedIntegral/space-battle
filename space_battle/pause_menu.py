import pygame_gui
from settings import *

class PauseMenu:
    def __init__(self):
        self.manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), theme_path="ui_theme.json")

        self.button_size = pg.Vector2(150, 50)
        window_center_x = WINDOW_SEMI_WIDTH - self.button_size.x / 2
        self.quit_button = pygame_gui.elements.UIButton(pg.Rect((window_center_x, 600), self.button_size), text="quit", manager=self.manager)
        self.key_bindings_button = pygame_gui.elements.UIButton(pg.Rect((window_center_x, 530), self.button_size), text="show key bindings", manager=self.manager)

        text = """
            pause: ESC
            accelerate: W
            deccelerate: S
            pull left: A
            pull right: D
            stability assist: SHIFT
            shoot: X
            toggle map: M
            dock: C
            center view: V
            pan view: LMB
            zoom: scroll
            map zoom: CTRL + scroll
        """
        self.key_bindings_info_box = pygame_gui.elements.UITextBox(text, relative_rect=pg.Rect((1200, 265), (300, 400)), manager=self.manager, visible=False)
    
    def update(self, app, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.quit_button:
                app.running = False
            
            elif event.ui_element == self.key_bindings_button:
                self.key_bindings_info_box.visible = not self.key_bindings_info_box.visible
        
        self.manager.process_events(event)

        self.manager.update(app.delta_t / 1000)

        self.manager.draw_ui(app.window)