import os, json

class Settings:

    _settings = {}

    def __init__(self):
        self.check_settings()

    def get_settings(self):
        return self._settings

    def set_city(self, city):
        self._settings["city"] = city
        self.save_settings()

    def save_settings(self):
        os_name = os.name
        if os_name == "nt":
            user = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
            with open(os.path.join(user, "newsettings.json"), 'w') as json_file:
                json.dump(self._settings, json_file)
        elif os_name == 'posix':
            home = os.path.expanduser('~')
            with open(os.path.join(home, "newsettings.json"), 'w') as json_file:
                json.dump(self._settings, json_file)

    def create_settings_file(self, settings_file):
            settings = {}
            settings["baseurl"] = "https://api.openweathermap.org/data/2.5/weather"
            settings["city"] = ""
            settings["appid"] = input("Enter your API key here: ")

            os_name = os.name
            if os_name == "nt":
                user = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
                with open(os.path.join(user, settings_file), 'a') as json_file:
                    json.dump(settings, json_file)
            elif os_name == 'posix':
                home = os.path.expanduser('~')
                with open(os.path.join(home, settings_file), 'a') as json_file:
                    json.dump(settings, json_file)


    def check_settings(self):
        settings_file = "newsettings.json"
        os_name = os.name
        if os_name == 'nt':
            user = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
            if  os.access(os.path.join(user, settings_file), os.R_OK):
                with open(os.path.join(user, settings_file), 'r') as json_file:
                    parser_data = json.load(json_file)
                    self._settings["baseurl"] = parser_data['baseurl']
                    self._settings["city"] = parser_data['city']
                    self._settings["appid"] = parser_data['appid']
            else:
                self.create_settings_file("newsettings.json")

        elif os_name == 'posix':
            home = os.path.expanduser('~')
            if os.access(os.path.join(home, settings_file), os.R_OK):
                with open(os.path.join(home, settings_file), 'r') as json_file:
                    parser_data = json.load(json_file)
                    self._settings["baseurl"] = parser_data['baseurl']
                    self._settings["city"] = parser_data['city']
                    self._settings["appid"] = parser_data['appid']
            else:
                self.create_settings_file("newsettings.json")
