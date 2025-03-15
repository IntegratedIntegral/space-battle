from button import Button

class LocationsMenu:
    def __init__(self, locations):
        self.location_buttons = self.generate_location_buttons(locations)
    
    @staticmethod
    def generate_location_buttons(locations):
        location_buttons = []
        for i in range(len(locations)):
            location = locations[i]
            location_buttons.append(Button((350, 280 + 60 * i), (80, 40), location["name"]))
        return location_buttons
    
    def update(self, app):
        for i in range(len(self.location_buttons)):
            button = self.location_buttons[i]
            location = app.locations[i]

            button.update(app.window, app.lmb_pressed)
            if button.pressed and location["name"] != app.world_objects.active_location_name:
                app.world_objects.set_location(location)
                app.locationsmenu_active = False