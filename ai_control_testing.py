import win32com.client

ai = win32com.client.Dispatch("Illustrator.Application")

# Create a new document called "blended_circles" with dimensions 30x30cm
doc = ai.Documents.Add(None, 30, 30, 1)

# Create the first circle
circle1 = ai.ActiveDocument.PathItems.Ellipse(0, 0, 5, 5)
circle1.FillColor = win32com.client.constants.aiColorRGB(0, 0, 0)

# Create the second circle
circle2 = ai.ActiveDocument.PathItems.Ellipse(10, 10, 2, 2)