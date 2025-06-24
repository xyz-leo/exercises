# Color Schemes with background colors for numbers, operators, font, and special characters. You can add or remove schemes.
COLOR_SCHEMES = {
    'DARK': {
        'num_bg_color': '#2E2E2E', 
        'operators_bg_color': '#4C4C4C', 
        'special_char_bg_color': '#666666', 
        'font_color': 'white'
    },
    'ORANGE': {
        'num_bg_color': '#FFA500', 
        'operators_bg_color': '#FF8C00', 
        'special_char_bg_color': '#FF7F50', 
        'font_color': 'white'
    },
    'PINK': {
        'num_bg_color': '#FFC0CB', 
        'operators_bg_color': '#FF69B4', 
        'special_char_bg_color': '#FF1493', 
        'font_color': 'black'
    },
    'BLUE': {
        'num_bg_color': '#ADD8E6', 
        'operators_bg_color': '#4682B4', 
        'special_char_bg_color': '#5F9EA0', 
        'font_color': 'black'
    },
    'GREEN': {
        'num_bg_color': '#98FB98', 
        'operators_bg_color': '#32CD32', 
        'special_char_bg_color': '#228B22', 
        'font_color': 'black'
    },
    'LIGHT': {
        'num_bg_color': '#ADD8E6', 
        'operators_bg_color': '#87CEEB', 
        'special_char_bg_color': '#B0E0E6', 
        'font_color': 'black'
    },
    'RED': {
        'num_bg_color': '#FF6347', 
        'operators_bg_color': '#FF4500', 
        'special_char_bg_color': '#DC143C', 
        'font_color': 'white'
    },
    'LIGHTBLUE': {
        'num_bg_color': '#B0E0E6', 
        'operators_bg_color': '#ADD8E6', 
        'special_char_bg_color': '#87CEEB', 
        'font_color': 'black'
    },
    'DARKBLUE': {
        'num_bg_color': '#1E3A5F', 
        'operators_bg_color': '#2C3E50', 
        'special_char_bg_color': '#34495E', 
'font_color': 'white'
    },
    'BLACKPINK': {
        'num_bg_color': '#333333', 
        'operators_bg_color': '#F06292', 
        'special_char_bg_color': '#D81B60', 
        'font_color': 'white'
    },
    'BABYPINK': {
        'num_bg_color': '#FADADD', 
        'operators_bg_color': '#FFB6C1', 
        'special_char_bg_color': '#FF69B4', 
        'font_color': 'black'
    }
}


class ButtonStyle():
    """
    A class responsible for styling buttons using different color schemes.
    It applies font styles and color schemes to the buttons.
    """
    def __init__(self, button):
        self.button = button # reference to the button
        self.fontStyle() # apply the font style


    def fontStyle(self, family="Arial", italic=True):
        """
        Applies font styling to the button, such as setting the font family and italic style.
        
        :param family: Font family to use (default is 'Arial').
        :param italic: Whether to use italic font style (default is True).
        """
        font = self.button.font()
        font.setFamily(family)
        font.setItalic(italic)
        self.button.setFont(font)


    # Method to apply a style to a button, used in "_createbuttons".
    def applyColorScheme(self, scheme_name, button_type):
        """
        Applies the color scheme to a button based on its type (number, operator, special character).
        
        :param scheme_name: The name of the color scheme (e.g., 'DARK', 'ORANGE').
        :param button_type: The type of the button (e.g., 'num_bg_color', 'operators_bg_color', 'special_char_bg_color').
        """
        color = COLOR_SCHEMES.get(scheme_name, COLOR_SCHEMES['DARK']) #Default
        
        # Applying themes
        self.button.setStyleSheet(f"background-color: {color[button_type]}; color: {color['font_color']};") #type: ignore
