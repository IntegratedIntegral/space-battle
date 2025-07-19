import os
from settings import *
from button import Button
from text_box import TextBox

class SaveMenu:
    def __init__(self):
        self.save_buttons, self.reset_buttons = self.generate_buttons()
        self.back_button = Button((WINDOW_SEMI_WIDTH - 160, 460), (150, 50), "back")

        self.reset_are_you_sure_text_box = TextBox((WINDOW_SEMI_WIDTH + 170, 0), (110, 23), "are you sure?")
        self.reset_yes_button = Button((WINDOW_SEMI_WIDTH + 170, 0), (53, 23), "yes")
        self.reset_no_button = Button((WINDOW_SEMI_WIDTH + 227, 0), (53, 23), "no")

        self.requesting_reset_confirmation = False
        self.reset_save_index: int = None
    
    def generate_buttons(self):
        save_buttons = []
        reset_buttons = []
        save_names = os.listdir(join("save_data"))
        for i in range(len(save_names)):         
            save_buttons.append(Button((WINDOW_SEMI_WIDTH - 160, 530 + 70 * i), (190, 50), ""))
            reset_buttons.append(Button((WINDOW_SEMI_WIDTH + 50, 530 + 70 * i), (110, 50), "reset"))
        return save_buttons, reset_buttons
    
    def button_text(self, locations: list[dict], save_data: dict):
        if save_data["started"]:
            total_bs_count = 0
            complete_bs_count = 0

            #count total battle sites
            for location in locations: total_bs_count += len(location["battle_sites"])

            #count completed battle sites
            for location_progress in save_data["battle_site_progress"].values():
                for bs_complete in location_progress: complete_bs_count += 1 if bs_complete else 0
            
            return f"{complete_bs_count}/{total_bs_count} battle sites completed"
        
        return "new game"
    
    def update_button_text(self, locations):
        save_names = os.listdir(join("save_data"))
        for i in range(len(self.save_buttons)):
            with open(join("save_data", save_names[i])) as file: save_data = json.load(file)
            self.save_buttons[i].set_text_surf(self.button_text(locations, save_data))
    
    def reset_save(self, locations: list[dict], save_name, button_index):
        save_data = {
            "started": False,
            "location_id": 0,
            "ship_name": "sunspot",
            "weapon_name": "radioactive A",
            "pos": None,
            "vel": None,
            "health": None,
            "battle_site_progress": {}
        }

        #reset battle site progress
        save_data["battle_site_progress"] = dict.fromkeys([location["name"] for location in locations])
        for i in range(len(locations)):
            location_name = locations[i]["name"]
            save_data["battle_site_progress"][location_name] = [False for battle_site in locations[i]["battle_sites"]]
        
        #store save data into json file
        with open(join("save_data", save_name), "w") as file: json.dump(save_data, file)
        self.save_buttons[button_index].set_text_surf(self.button_text(locations, save_data))
    
    def request_reset_confirmation(self, index):
        #make text box and yes and no buttons appear and set their y positions
        self.reset_are_you_sure_text_box.pos = (self.reset_are_you_sure_text_box.pos[0], 530 + 70 * index)
        self.reset_yes_button.rect.y = 557 + 70 * index
        self.reset_no_button.rect.y = 557 + 70 * index
        self.requesting_reset_confirmation = True
        self.reset_save_index = index
    
    def update(self, app):
        self.back_button.update(app.window, app.lmb_pressed)

        for i in range(len(self.save_buttons)):
            save_button = self.save_buttons[i]
            reset_button = self.reset_buttons[i]

            #LOAD SAVE BUTTONS
            save_button.update(app.window, app.lmb_pressed)
            if save_button.just_pressed:
                saves = os.listdir(join("save_data"))
                save_name = saves[i]
                with open(join("save_data", save_name)) as file: save_data = json.load(file)
                app.load_world(save_data, save_name)

            #RESET SAVE BUTTONS
            reset_button.update(app.window, app.lmb_pressed)
            if reset_button.just_pressed: self.request_reset_confirmation(i)

        #BACK BUTTON
        if self.back_button.just_pressed:
            app.savemenu_active = False
            app.mainmenu_active = True
        
        if self.requesting_reset_confirmation:
            #RESET YES/NO BUTTONS
            self.reset_are_you_sure_text_box.draw(app.window)
            self.reset_yes_button.update(app.window, app.lmb_pressed)
            self.reset_no_button.update(app.window, app.lmb_pressed)

            if self.reset_yes_button.just_pressed:
                self.requesting_reset_confirmation = False
                save_names = os.listdir(join("save_data"))
                self.reset_save(app.locations, save_names[self.reset_save_index], self.reset_save_index)
            
            elif self.reset_no_button.just_pressed: self.requesting_reset_confirmation = False