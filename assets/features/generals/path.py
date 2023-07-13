import json


def get_config():
    with open("assets/config/env.json", encoding="utf-8") as fh:
        json_txt = fh.read()
        json_txt = (
            str(json_txt)
            .replace("'", '"')
            .replace("True", "true")
            .replace("False", "false")
        )
        config = json.loads(json_txt)
        return config


class ControlConfig:
    def __init__(self):
        self.config = get_config()

    def get_token(self):
        return self.config["token"]

    def get_prefix(self):
        return self.config["prefix"]

    def __get_abs(self, path_text):
        return self.config["paths"]["absolute"] + path_text

    def get_bg(self, index):
        path_bg = self.config["paths"]["background"] + f"background_{index}.png"
        return self.__get_abs(path_bg)

    def get_db(self):
        path_db = self.config["paths"]["database"]
        return self.__get_abs(path_db)

    def get_none(self):
        path_none = self.config["paths"]["none"]
        return self.__get_abs(path_none)

    def get_treasure_box(self):
        path_treasure_box = self.config["paths"]["treasure_box"]
        return self.__get_abs(path_treasure_box)

    def get_shop(self):
        path_shop = self.config["paths"]["shop"]
        return self.__get_abs(path_shop)

    def get_akuma(self):
        path_akuma = self.config["paths"]["akuma"]
        return self.__get_abs(path_akuma)

    def get_playing(self, user_id):
        path_playing = self.config["paths"]["playing"] + f"{user_id}.png"
        return self.__get_abs(path_playing)
