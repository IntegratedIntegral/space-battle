from settings import *
from button import Button
from text_box import TextBox
from paragraph_line_break import line_break

class LocationsMenu:
    def __init__(self, locations):
        self.title_box = TextBox((WINDOW_SEMI_WIDTH - 120, 390), (80, 30), "locations")
        self.location_buttons = self.generate_location_buttons(locations)
        self.info_box_default_text = "Select a location to travel to"
        self.info_box = TextBox((WINDOW_SEMI_WIDTH + 50, 390), (200, 160), self.info_box_default_text)
    
    @staticmethod
    def generate_location_buttons(locations):
        location_buttons = []
        for i in range(len(locations)):
            location = locations[i]
            location_buttons.append(Button((WINDOW_SEMI_WIDTH - 120 , 440 + 60 * i), (80, 40), location["name"]))
        return location_buttons
    
    def update(self, app):
        self.title_box.draw(app.window)

        self.info_box.draw(app.window)
        self.info_box.set_text_surf(self.info_box_default_text)

        for i in range(len(self.location_buttons)):
            button = self.location_buttons[i]
            location = app.locations[i]

            button.update(app.window, app.lmb_pressed)
            if button.pressed and location["name"] != app.world_objects.active_location["name"]:
                #set location
                app.world_objects.set_location(app.save_data, location)
                app.locationsmenu_active = False
            
            #button hovered. display description of that location
            if button.hovered: self.info_box.set_text_surf(location["name"] + ":\n" + line_break(location["description"], UI_FONT, self.info_box.surf.width))