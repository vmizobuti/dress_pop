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
from Rhino.Geometry import Point3d, Vector3d, Hatch, Curve

def c2p(number):
    """
    Converts a number from centimeters to point units.
    """
    # Declares the conversion factor
    factor = 28.3465

    # Converts the number from centimeters to points
    conversion = number * factor

    return conversion

def make_art(filename, width, height, margins):
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
    doc.Views.ActiveView.ActiveViewport.PushViewInfo(Rhino.DocObjects.ViewInfo(viewport), False)
    
    # Turns every closed Curve into a Hatch
    for layer in doc.Layers:
        doc.Layers.SetCurrentLayerIndex(layer.Index, True)
        curves = doc.Objects.FindByLayer(layer)
        for curve in curves:
            if curve.Geometry.IsClosed == True:
                hatch = Hatch.Create(curve.Geometry, 1, 0, 1, 0.01)
                doc.Objects.AddHatch(hatch[0])
                doc.Objects.Delete(curve)
            else:
                continue

    # Exports the AI file
    ai_file = getcwd() + "\\" + "art.ai"
    doc.Export(ai_file)

    # Instantiates an Application of Adobe Illustrator
    ai = win32.Dispatch("Illustrator.Application")

    # Converts the width and height values to points
    canvas_width = c2p(width)
    canvas_height = c2p(height)

    # Opens the art.ai document
    art_filename = getcwd() + "\\" + "art.ai"
    art_doc = ai.Open(art_filename)
    
    # Adds a new artboard to the file given width and height values
    rect_a = -canvas_width/2
    rect_b = canvas_height/2
    rect_c = canvas_width/2
    rect_d = -canvas_height/2
    rect = (rect_a, rect_b, rect_c, rect_d)
    canvas = art_doc.Artboards.Add(rect)
    canvas.Name = "DressPOP"
    
    # Deletes the old artboard (for some reason I can't resize it using COM)
    art_doc.Artboards.GetByName("Artboard 1").Delete()

    # Adjusts the main waveline stroke width
    for layer in art_doc.Layers:
        if layer.Name == "Stroke":
            layer.PathItems.Item(1).StrokeWidth = height/2
    
    # Groups all objects and aligns it to center of the artboard
    group = art_doc.GroupItems.Add()
    for path in range(art_doc.PathItems.Count):
        art_doc.PathItems[path + 1].Move(group, 1)
    top_pos_x = c2p(margins) - canvas_width/2
    top_pos_y = canvas_height/2 - c2p(margins)
    group.Position = (top_pos_x, top_pos_y)

    # Exports the file as a PDF
    options = win32.Dispatch("Illustrator.PDFSaveOptions")
    savefile = getcwd() + "\\" + "art.pdf"
    art_doc.SaveAs(savefile, options)

    # Quits the Illustrator Application
    ai.Quit()

    # Deletes all used files
    remove(getcwd() + "\\" + "art.ai")
    remove(getcwd() + "\\" + "geometry.3dm")