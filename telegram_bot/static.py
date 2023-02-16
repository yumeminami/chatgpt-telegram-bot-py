import os
import json


class Text():
    def __init__(self,language:str):
        if language == "":
            self.language = "en"
        data = json.load(open("config/config.json"))

        self.main_menu_text = data["main_menu_text"]["en"]
        self.chat_usage_text = data["conversation_usage_text"]["en"]
        self.create_usage_text = data["images_usage_text"]["en"]
        self.gpt_3_intro_text = data["gpt_3_intro_text"]["en"]
        self.dalle_intro_text = data["dalle_intro_text"]["en"]
        self.stability_disfussion_text = data["stability_disfussion_text"]["en"]
        
        self.chat_button_text = data["conversation_button_text"]["en"]
        self.create_button_text = data["images_button_text"]["en"]

    def change_language(self,language:str):
        if language == "":
            self.language = "en"
        data = json.load(open("config/config.json"))

        self.main_menu_text = data["main_menu_text"][language]
        self.chat_usage_text = data["conversation_usage_text"][language]
        self.create_usage_text = data["images_usage_text"][language]
        self.gpt_3_intro_text = data["gpt_3_intro_text"][language]
        self.dalle_intro_text = data["dalle_intro_text"][language]
        self.stability_disfussion_text = data["stability_disfussion_text"][language]
        
        self.chat_button_text = data["conversation_button_text"][language]
        self.create_button_text = data["images_button_text"][language]


