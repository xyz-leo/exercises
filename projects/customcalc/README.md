# CustomCalc
Custom Calculator App Made in Python with PySide6

# CustomCalc
A project of a custom calculator made in Python, by me. You can change the calculator themes and size. Please enjoy!

Calculator App Interface:

![image](https://github.com/user-attachments/assets/a454e2e6-4791-46ff-876c-044741335f35) ![image](https://github.com/user-attachments/assets/8a275c79-0ab8-4e9b-9f2c-323aa21453ae)
 ![image](https://github.com/user-attachments/assets/1d29bc37-000e-47cc-9c75-797fe60fd1b4) 



This is a simple calculator app developed with Python and the PySide6 library. The app features an intuitive graphical user interface (GUI) and allows users to perform basic mathematical operations such as addition, subtraction, multiplication, division, exponentiation, percentage, along with functionalities like clearing the display and deleting a character at a time.

Features

    Basic mathematical operations: Addition, subtraction, multiplication, division.

    Exponentiation (^).

    Percentage (%).

    Clear display (C).

    Delete last character (⌫).

    Responsive calculator: The interface adjusts for different screen sizes, with customizable color schemes and button sizes.


Technologies Used

    Python 3.13.2

    PySide6: Framework for building graphical user interfaces.

    JSON: Used to save user settings, such as theme and button size.


How to Run the Project

    1. Clone the repository:

    git clone https://github.com/xyz-leo/CustomCalc.git
    
    2. cd CustomCalc
    Create a Python virtual environment
    After activating the virtual environment: pip install -r requirements.txt

    Then, run it with: python3 main.py
    This will launch the calculator's graphical interface.


Customization

The app allows customization of the theme and button sizes


Themes

Currently, the following themes are supported:

    DARK

    ORANGE

    PINK

    BLUE

    GREEN

    LIGHT

    RED

    LIGHTBLUE

    DARKBLUE

    BLACKPINK

    BABYPINK


Button Sizes

You can adjust the button sizes with the following schemes

    SMALL

    MEDIUM

    LARGE

These preferences are saved in a configuration file, config.json, located in the files folder.
Project Structure

    main.py: The main file that initializes the application.

    buttons.py: Contains the Button class for creating and managing the calculator buttons.

    display.py: Creates the screen display and the info display of the calculator.

    central_window.py: Manages the window of the calculator.
    
    utils.py: Helper functions like expression validation and safe evaluation.

    themes.py: Defines color schemes for UI customization.

    config.py: Loads and saves user theme and size preferences.

    size_manager.py: Manages different size schemes to the entire application.


How to Contribute

    Fork this repository.

    Create a new branch for your changes (git checkout -b feature/new-feature).

    Commit your changes (git commit -am 'Add new feature').

    Push to the branch (git push origin feature/new-feature).

    Open a pull request.
