#================================= IMPORTS ====================================#
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMenu
from PySide6.QtCore import QCoreApplication, QProcess
from PySide6.QtGui import QIcon, QAction
from utils import WINDOW_ICON_PATH
from config import Config
from size_manager import SIZE_SCHEMES
from themes import COLOR_SCHEMES
import sys
#===============================================================================#

# This class is responsible for the calculator window.
class MainWindow(QMainWindow):
    def __init__(self, size_manager, config: Config, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        # Creating an instance of the QWidget, that contains what we need to manipulate the windows.
        self.centralWindow = QWidget()

        # Window Title 
        self.setWindowTitle('Custom Calculator')

        # Setting icon for the application
        icon = QIcon(str(WINDOW_ICON_PATH))
        self.setWindowIcon(icon)
        self.add_top_buttons()
 

        # Module references
        self.config = config 
        self.size_manager = size_manager


        # Primary Layout (vertical)
        self.verticalLayout = QVBoxLayout()
        self.centralWindow.setLayout(self.verticalLayout)
        self.setCentralWidget(self.centralWindow)
        
               
        # Setting the window size (width and height) calling the method get_size of the Size Manager class
        window_width, window_height = self.size_manager.get_size("window_size")
        
        self.resize(window_width, window_height) # Applying the window size and resizing it
        
        self.adjustFixedSize() # Calling this method to fix the window size
        
        
    # Method to add widgets to the vertical (main) layout
    def addWidgetToVerticalLayout(self, widget: QWidget):
        self.verticalLayout.addWidget(widget)


    # Ensures a fixed size is applied, which means you cannot change the window size manually.
    def adjustFixedSize(self):
        self.setFixedSize(self.width(), self.height())


    def add_top_buttons(self):
        menu_bar = self.menuBar() # Creating a menu bar and adding actions
        
        # Creating a button for size options
        size_button = QAction("Size", self)
        size_menu = QMenu(self)
        size_button.setMenu(size_menu)


        # Creating a button for theme options
        theme_button = QAction("Theme", self)
        theme_menu = QMenu(self)
        theme_button.setMenu(theme_menu)


        # Adding theme and size options
        for theme_name in COLOR_SCHEMES.keys():
            action = QAction(theme_name, self)
            action.triggered.connect(lambda checked, t=theme_name: self.change_theme(t)) 
            theme_menu.addAction(action)

        for size_name in SIZE_SCHEMES.keys():
            action = QAction(size_name, self)
            action.triggered.connect(lambda checked, s=size_name: self.change_size(s))
            size_menu.addAction(action)


        # Adding buttons to the menu bar at the right corner
        menu_bar.addAction(size_button)
        menu_bar.addAction(theme_button)
        

    def change_theme(self, theme_name):
        # Change the calculator theme and save it in the config.json file.
        self.config.set_theme(theme_name)
        self.restart_app()
        

    def change_size(self, size_name):
        # Change the calculator size and resize the window.
        self.config.set_size(size_name)
        self.restart_app()


    # Restarting the app to apply changes
    def restart_app(self):
        QCoreApplication.quit()
        QProcess.startDetached(sys.executable, sys.argv) # type: ignore
