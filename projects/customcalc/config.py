#=================================== IMPORTS =================================#
from pathlib import Path
import json
from themes import COLOR_SCHEMES
from size_manager import SIZE_SCHEMES
#=============================================================================#

# Using Path to locate the icon and the config file
ROOT_DIR = Path(__file__).parent
FILES_DIR = ROOT_DIR / 'files'
CONFIG_PATH = FILES_DIR / 'config.json'


class Config:
    def __init__(self):
        self.config_data = self.load_config() # Load the saved config

    def load_config(self):
        # Load the JSON config file
        try:
            with open(CONFIG_PATH, 'r') as file:
                config = json.load(file)

                config.setdefault("theme", "DARK")
                config.setdefault("size", "MEDIUM")
                return config
        except FileNotFoundError:
            return {
                    'theme': 'DARK', # Standard theme
            }


    def save_config(self):
        # Save the config in the JSON file
        with open(CONFIG_PATH, 'w') as file:
            json.dump(self.config_data, file, indent=4)


    def get_theme(self):
        # Return the current theme
        return self.config_data.get('theme', 'DARK')


    def set_theme(self, theme_name):
        # Define a new theme and save the configuration
        if theme_name in COLOR_SCHEMES:
            self.config_data['theme'] = theme_name
            self.save_config()
        else:
            print(f"Error: theme: '{theme_name}' not found.")
            self.config_data['theme'] = "DARK"

    
    def get_size(self):
        # Return the current size of the application
        return self.config_data.get('size', 'MEDIUM')
 

    def set_size(self, size_name):
        if size_name in SIZE_SCHEMES:
            self.config_data['size'] = size_name
            self.save_config()
        else:
            print(f"Error: size {size_name}' not found.")
            self.config_data['theme'] = "MEDIUM"

    
    def get_avaiable_themes(self):
        return list(COLOR_SCHEMES.keys())

    def get_avaiable_sizes(self):
        return list(SIZE_SCHEMES.keys())
