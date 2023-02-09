import win32com.client as win32

def c2p(number):
    """
    Converts a number from centimeters to point units.
    """
    # Declares the conversion factor
    factor = 28.346

    # Converts the number from centimeters to points
    conversion = number * factor

    return conversion

def make_art(width, height, text):
    """
    Makes an art in Adobe Illustrator using the generative parameters.
    The art will have a size of width and height, and the text is
    the input for the generative system.
    """
    print("Hello.")