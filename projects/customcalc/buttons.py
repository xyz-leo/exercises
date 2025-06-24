#================================= IMPORTS =====================================#
from PySide6.QtWidgets import QGridLayout, QPushButton 
from PySide6.QtCore import Signal
from utils import NUM_OR_DOT, OPERATORS, SPECIAL_CHAR, matchesRegex, isValidExpression, safe_eval
from themes import ButtonStyle
#===============================================================================#

# Button Superclass, responsible for the buttons behavior.
class Button(QPushButton):
    # Create a signal to send the button text
    clickedButton_text = Signal(str)
    
    def __init__(self, text, size_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Creating an instance of ButtonStyle. Responsible for stylizing the buttons, like the font and background color
        self.button_style = ButtonStyle(self)
        
        # The text of the button
        self.setText(text)

        # Setting the clicked event to the method on_click
        self.clicked.connect(self._on_click) # ^ Connecting the click event
        
        # Creating three variables, they are responsible for applying the correct size to the buttons. We get those values calling the method of the Size Manager class, which will return the sizes.
        button_width, button_height, button_font_size = size_manager.get_size("button_size")

        # Applying the size to the button
        self.setFixedSize(button_width, button_height)
        
        # Applying the size to the font of the button
        font = self.font()
        font.setPointSize(button_font_size)
        self.setFont(font)
        
        
    # When a button is clicked, this function is called
    def _on_click(self):
        # Emits a signal that contains the button text
        self.clickedButton_text.emit(self.text())


# Class responsible for "drawing" the buttons. It creates an instance of each button.
class ButtonsGrid(QGridLayout):
    def __init__(self, calcdisplay, top_display, color_scheme, size_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Matrix with the calculator text buttons.
    # You can change this layout as you wish, but be careful if so.
        self.buttons = [
            ['^', 'C', '⌫', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '−'],
            ['1', '2', '3', '+'],
            ['%', '0', '.', '='],
        ]
        
        self.calcdisplay = calcdisplay # reference to the display
        self.top_display = top_display # reference to the info
        
        # The method creates each object of the buttons.
        self._create_buttons(color_scheme, size_manager)

        # 
        self.buttonFunctions = ButtonFunctions(calcdisplay, top_display) 


    def _buttonAction(self, button_text):
        actions = {
            'C': self.buttonFunctions._clear_display,
            '⌫': self.buttonFunctions._backspace,
            '=': self.buttonFunctions._calculate,
            '%': self.buttonFunctions._percentage
                }

        if button_text in actions:
            actions[button_text]()
        else:
            self._update_calcdisplay(button_text)

      
    # this method updates the display with the clicked button
    def _update_calcdisplay(self, text):
            current_text = self.calcdisplay.text()
            new_text = current_text + text
            
            # Validating the expression before updating the display
            if isValidExpression(new_text):
                self.calcdisplay.setText(new_text)
            #else:
                #print(f"Invalid input! {new_text}") # Debug


    def _update_topdisplay(self, text):
        current_text = self.top_display.text()
        self.top_display.setText(current_text + text)


    # This method creates the calculator buttons.
    def _create_buttons(self, color_scheme, size_manager):
        # Traversing the matrix that contains the button text to generate the buttons.
        for row, line in enumerate(self.buttons):
            for col, button_text in enumerate(line):
                if button_text:  # This 'if' avoid creating blank buttons
                    # Creating the instance of the button.
                    button = Button(button_text, size_manager)
                    button.clickedButton_text.connect(lambda text=button_text: self._buttonAction(text))

                    # Button of the numbers and the dot
                    if matchesRegex(NUM_OR_DOT, button_text):
                        button.button_style.applyColorScheme(color_scheme, "num_bg_color")
                  
                    # Button of the mathematical operators
                    if matchesRegex(OPERATORS, button_text):
                        button.button_style.applyColorScheme(color_scheme, "operators_bg_color")
                   
                    # Button of the special characters like C, and the backspace
                    if matchesRegex(SPECIAL_CHAR, button_text):
                        button.button_style.applyColorScheme(color_scheme, "special_char_bg_color")
                 
                 # Adding the created button widget to the interface
                    self.addWidget(button, row, col)


# Class to define the button action when they are clicked 
class ButtonFunctions:
    def __init__(self, calcdisplay, top_display):
        # Storing the needed references
        self.calcdisplay = calcdisplay
        self.top_display = top_display


    def _clear_display(self):
        self.calcdisplay.clear()  # clear the display


    def _backspace(self):
        current_text = self.calcdisplay.text()
        self.calcdisplay.setText(current_text[:-1])  # Delete the last character


    def _calculate(self):
        expression = self.calcdisplay.text()
        # Replacing the operator text to the Python operators.
        expression = expression.replace('÷', '/').replace('×', '*').replace('−', '-')

        try:
            result = safe_eval(expression)  # Function to eval the expression
            self.calcdisplay.setText(str(result))  # Show the result in the calculator display
            self.top_display.setText(expression + " = " + str(result)) # Show the result in the top display of the calculator.
        except Exception:
            # If the user tries a invalid expression, it shows an Error message in the top display, then, clears the calculator display.
            self.top_display.setText("Error")
            self._clear_display()


    def _percentage(self):
        current_text = self.calcdisplay.text()
        try:
            result = float(current_text) / 100  # Converts to percentage 
            self.calcdisplay.setText(str(result))  # Show the result in the calculator display
        except Exception:
            self.top_display.setText("Error")
            self._clear_display()
 
