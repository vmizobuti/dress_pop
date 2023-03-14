# make_art.py
#
# Functions for generating an art in Adobe Illustrator
# based on a set of colors and sound parameters.

from os import remove, getcwd
import win32com.client as win32
import rhinoinside

rhinoinside.load()

import System
import Rhino
from Rhino.Geometry import Point3d, Vector3d

def c2p(number):
    """
    Converts a number from centimeters to point units.
    """
    # Declares the conversion factor
    factor = 28.3465

    # Converts the number from centimeters to points
    conversion = number * factor

    return conversion

def make_art(filename, width, height):
    """
    Makes an art in Adobe Illustrator by using a .3DM file's geometry.
    The art will have a size of width and height, and 
    """
    # Opens the 3DM file
    doc = Rhino.RhinoDoc.Open(getcwd() + "\\" + filename)[0]

    # Sets the viewport to Top View
    viewport = Rhino.Display.RhinoViewport()
    viewport.SetToPlanView(Point3d(0, 0, 0), 
                           Vector3d(1, 0, 0),
                           Vector3d(0, 1, 0), True)
    doc.Views.ActiveView = 
    doc.Views.Redraw()
    ai_file = getcwd() + "\\" + "art.ai"
    doc.Export(ai_file)

    # Instantiates an Application of Adobe Illustrator
    #ai = win32.Dispatch("Illustrator.Application")

    # Converts the width and height values to points
    canvas_width = c2p(width)
    canvas_height = c2p(height)

    # Creates a new document using the CMYK color space
    #doc = ai.Documents.Add(2, canvas_width, canvas_height)
