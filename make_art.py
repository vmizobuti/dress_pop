# make_art.py
#
# Functions for generating an art in Adobe Illustrator
# based on a set of colors and sound parameters.

from os import remove, getcwd
from math import ceil
import rhinoinside


rhinoinside.load()

import System
import Rhino
from Rhino.Geometry import Point3d, Vector3d, Hatch

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
    doc.Views.ActiveView.ActiveViewport.PushViewInfo(Rhino.DocObjects.ViewInfo(viewport), False)
    
    # Turns every closed Curve into a Hatch
    for layer in doc.Layers:
        doc.Layers.SetCurrentLayerIndex(layer.Index, True)
        if layer.Name == 'Frame':
            continue
        else:
            curves = doc.Objects.FindByLayer(layer)
            for curve in curves:
                if curve.Geometry.IsClosed == True:
                    hatch = Hatch.Create(curve.Geometry, 1, 0, 1, 0.01)
                    doc.Objects.AddHatch(hatch[0])
                    doc.Objects.Delete(curve)
                else:
                    continue

    # Instantiates the output PDF file
    pdf = Rhino.FileIO.FilePdf.Create()

    # Defines the settings for the PDF file
    view = doc.Views.ActiveView
    dpi = 300
    px_width = ceil((width/2.54) * dpi)
    px_height = ceil((height/2.54) * dpi)
    size = System.Drawing.Size(px_width, px_height)
    settings = Rhino.Display.ViewCaptureSettings(view, size, dpi)
    settings.RasterMode = False
    settings.ViewArea = Rhino.Display.ViewCaptureSettings.ViewAreaMapping(1)
    pdf.AddPage(settings)

    # Saves the PDF file at a given path
    path = getcwd() + "\\" + "art.pdf"
    pdf.Write(path)

    remove(getcwd() + "\\" + "geometry.3dm")

    return