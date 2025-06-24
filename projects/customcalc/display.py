from PySide6.QtWidgets import QLineEdit, QLabel, QWidget
from PySide6.QtCore import Qt

# Display of the calculator ("the screen with the numbers, etc")
class CalculatorDisplay(QLineEdit):
    def __init__(self, size_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This will make the display read only. This also provides more security
        self.setReadOnly(True)
        
        display_width, display_height, display_font_size = size_manager.get_size("calc_display_size") # Getting the size of the display
        
        self.setFixedSize(display_width, display_height)
        
        font = self.font()
        font.setPointSize(display_font_size)
        self.setFont(font)
        
        self.setAlignment(Qt.AlignmentFlag.AlignRight) # The text alignment will be on the right side


# Top display for showing expression or additional info
class TopDisplay(QLabel):
    def __init__(self, text: str, size_manager, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self._config_style(size_manager)
        self.setAlignment(Qt.AlignmentFlag.AlignRight) # The text alignment will be on the right side
    

    # top_display font size and allignment 
    def _config_style(self, size_manager):
        top_display_width, top_display_height, top_display_font_size = size_manager.get_size("top_display_size")
        
        self.setFixedSize(top_display_width, top_display_height)
        
        font = self.font()
        font.setPointSize(top_display_font_size)
        self.setFont(font)
