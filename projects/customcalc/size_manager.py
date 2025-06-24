# This module provides an easy way to modify the size of everything in the software.

# SIZE SCHEMES / WIDTH, HEIGHT, FONT 
SIZE_SCHEMES = {
        'SMALL': {'button_size': (55, 40, 13), 'calc_display_size': (235, 50, 25), "top_display_size": (235, 16, 12), "window_size": (250, 320)},

        'MEDIUM': {'button_size': (70, 45, 16), 'calc_display_size': (295, 65, 35), "top_display_size": (290, 20, 13), "window_size": (310, 360)},

        'LARGE': {'button_size': (85, 60, 20), 'calc_display_size': (345, 75, 45), "top_display_size": (340, 40, 16), "window_size": (360, 460)},
}

# Class responsible to handle the size management of the software
class SizeManager:
    def __init__(self, size="MEDIUM"): # MEDIUM set as the default size
        self.set_size(size)

        
    def set_size(self, size):
        if size in SIZE_SCHEMES:
            self.config = SIZE_SCHEMES[size]
        else:
            raise ValueError(f"Invalid size '{size}'. Choose SMALL, MEDIUM or BIG.")


    def get_size(self, obj_size, *args):
        if obj_size not in self.config:
            raise ValueError(f"Invalid size key '{obj_size}'. Avaiable keys: {list(self.config.keys())}")
        
        # If it has not args, it means it was passed just one parameter to config. Example: Just resizing the width.
        if not args:
            return self.config[obj_size]
        else:
            if args[0] not in self.config:
                raise ValueError(f"Invalid size key '{obj_size}'. Avaiable keys: {list(self.config.keys())}")
            return self.config[obj_size], self.config[args[0]] # Resizing width and height
