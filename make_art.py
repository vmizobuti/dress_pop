import win32com.client as win32

def c2p(number):
    """
    Converts a number from centimeters to point units.
    """
    # Declares the conversion factor
    factor = 28.3465

    # Converts the number from centimeters to points
    conversion = number * factor

    return conversion

def make_art(colors, width, height):
    """
    Makes an art in Adobe Illustrator using the generative parameters.
    The art will have a size of width and height, and the text is
    the input for the generative system.
    """
    
    # Instantiates an Application of Adobe Illustrator
    ai = win32.Dispatch("Illustrator.Application")

    # Converts the width and height values to points
    canvas_width = c2p(width)
    canvas_height = c2p(height)

    # Defines the size of the rectangle shape given the
    # boundaries of the canvas
    lat_space = 2
    rect_width = c2p(width - lat_space)
    rect_height = c2p(height/10)

    # Creates a new document using the CMYK color space
    doc = ai.Documents.Add(2, canvas_width, canvas_height)

    # Creates a rectangle and aligns it to the center of the canvas
    top_coord = canvas_height/2 + rect_height/2
    left_coord = c2p(lat_space/2)
    rectangle = doc.PathItems.Rectangle(top_coord, 
                                        left_coord, 
                                        rect_width, 
                                        rect_height)
    
    # Creates the gradient fill from the list of colors
    gradient_colors = []
    for color in colors:
        ai_color = win32.Dispatch("Illustrator.RGBColor")
        ai_color.Red = color[0]
        ai_color.Green = color[1]
        ai_color.Blue = color[2]
        gradient_colors.append(ai_color)
    
    gradient = doc.Gradients.Add()
    gradient.Type = 2

    # Modifies the gradient for each color in colors
    for i in range(len(colors)):
        color_i = gradient.GradientStops.Add()
        color_i.RampPoint = 100/(len(colors) - 1) * i
        color_i.Color = gradient_colors[i]
    
    # Changes the shape color to the newly created gradient
    gradientColor = win32.Dispatch("Illustrator.GradientColor")
    gradientColor.Gradient = gradient
    gradientColor.Origin = [0.0, 0.0]
    gradientColor.HiliteLength = c2p(120)
    rectangle.FillColor = gradientColor
    rectangle.Stroked = False