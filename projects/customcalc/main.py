#========================= IMPORTS ================================#
import sys
from PySide6.QtWidgets import QApplication
from central_window import MainWindow 
from display import CalculatorDisplay, TopDisplay
from buttons import ButtonsGrid
from size_manager import SizeManager
from config import Config
#==================================================================#

if __name__ == '__main__':
    # Creating the main object of Qt Application
    app = QApplication(sys.argv)
    

    # Creating an instance of the config file.
    config = Config()
    
    
    #apply theme
    app_theme = config.get_theme()
    app_size = config.get_size()


    # Creating an instance of the size manager and passing the size as argument.
    size_manager = SizeManager(app_size)


    # Creating an instance of the MainWindow.
    window = MainWindow(size_manager, config)
    

#=========================== INTERFACE =============================#
    
    # The top display of the calculator. Shows the previous operation
    top_display = TopDisplay('', size_manager)
    window.addWidgetToVerticalLayout(top_display)


    # Display (Calculator Screen)
    display = CalculatorDisplay(size_manager)
    window.addWidgetToVerticalLayout(display)
   

    # Creating an instance of ButtonsGrid, responsible for "drawing" the calculator buttons on the interface
    buttons_grid = ButtonsGrid(display, top_display, app_theme, size_manager)
    

    # Adding the buttons_grid layout to the main layout
    window.verticalLayout.addLayout(buttons_grid)

#===================================================================#
    
    #displaying the window and execcuting the app in an event loop
    window.show()
    app.exec()
