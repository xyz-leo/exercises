#================================== IMPORTS ===================================#
import re
import operator
from pathlib import Path
#===============================================================================#

NUM_OR_DOT = re.compile(r'^[0-9.]$') # Matches digits or dot
OPERATORS = re.compile(r'^[÷−×=+%^]$') # Matches mathematical operators
SPECIAL_CHAR = re.compile(r'^[C⌫]$') # Matches special characters like clear function
OPERATORS_ITERABLE = {'.', '^', 'C', '⌫', '÷', '−', '×', '=', '+', '%'}


# Directories for locating the calculator icon
ROOT_DIR = Path(__file__).parent
FILES_DIR = ROOT_DIR / 'files'
WINDOW_ICON_PATH = FILES_DIR / 'ico.png'


# Verify if the item corresponds to the regex pattern (number or operator)
def matchesRegex(pattern, string: str) -> bool:
    """
    Verifies if the given string matches the specified regex pattern.
    
    :param pattern: Regex pattern to match.
    :param string: String to check.
    :return: True if the string matches the pattern, False otherwise.
    """
    return bool(pattern.search(string))


# Function to validate the mathematical expression
def isValidExpression(expression) -> bool:
    """
    Verifies if the mathematical expression is valid.
    
    Validity checks:
    - No consecutive operators (e.g., '++', '--').
    - Expression should not start with an operator (except '-').
    - No consecutive dots (e.g., '..').
    
    :param expression: The mathematical expression as a string.
    :return: True if the expression is valid, False otherwise.
    """
    if re.search(r"[÷−×=+^%]{2,}", expression): # Consecutive operators
        return False
   
    if not expression: # Empty expression is invalid
        return False

    if expression[0] in OPERATORS_ITERABLE and expression[0] != '−': # Avoid begin with an operator (except '-')
        return False

    if ".." in expression: # Avoid two decimal dots in a row
        return False
    return True
    

def safe_eval(expression):
    """
    Evaluates the mathematical expression safely.
    
    Replaces operators and calculates the result using a safe eval method.
    
    :param expression: The mathematical expression as a string.
    :return: The result of the evaluated expression.
    :raises ValueError: If the expression is invalid or cannot be evaluated.
    """
    # Map operators to Python operators
    operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '**': operator.pow,
            '%': operator.mod,
            }

    # Replaces ^ with  ** for exponentiation
    expression = expression.replace('^', '**')

    # Tokenize the expression, keeping operators as seperate tokens
    tokens = re.split(r'(\*\*|[%^*/+-])', expression)
    tokens = [t.strip() for t in tokens if t.strip()]

    if not tokens: # If no tokens were found, raise an error
        raise ValueError("Empty expression")

    # Initialize the total with the first number
    total = float(tokens[0])

    try:
        for i in range(1, len(tokens), 2):
            operator_ = tokens[i]
            next_number = float(tokens[i + 1])
            total = operators[operator_](total, next_number)
        return total
    except (IndexError, ValueError, ZeroDivisionError) as e:
        raise ValueError(f"Invalid expression: {e}")

