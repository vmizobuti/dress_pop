# make_rhino.py
#
# Functions for generating the art using RhinoScript.
# The generative system is based on a set of sound parameters.

import rhino3dm as r3dm
import compute_rhino3d.Util

from compute_rhino3d import Curve, Brep, AreaMassProperties

def remap(value, old_domain, new_domain):
    """
    Remaps a number between different domains.
    """

    # Compute the old domain's range
    old_range = old_domain[1] - old_domain[0]

    # Compute the new domain's range
    new_range = new_domain[1] - new_domain[0]

    # Remaps the value between domains
    remapped_value = (((value - old_domain[0]) * new_range)/old_range) + \
                     new_domain[0]

    return remapped_value

def make_rhino(parameters, width, height, colors, filename):

    # Instantiates the Rhino.Compute geometry server
    compute_rhino3d.Util.url = "http://localhost:8081/"

    # Creates the 3DM file for all geometric operations
    model = r3dm.File3dm()

    # Creates the Layers for each color in the art
    for i in range(len(colors)):
        red = colors[i][0]
        green = colors[i][1]
        blue = colors[i][2]
        alpha = 255 
        model.Layers.AddLayer("Color " + str(i), (red, green, blue, alpha))

    # Creates the data chunks for point coordinates
    number_of_columns = 23
    chunk_size = round(len(parameters)/number_of_columns)
    partitions = [parameters[i:i + chunk_size] for i in \
                  range(0, len(parameters), chunk_size)]
    
    # Sums all values of the chunks to create the curve parameters
    sum_values = []
    for list in partitions:
        sum_values.append(sum(list))

    # Remap the chunks values based on the height of the canvas
    amplitude_factor = 0.4
    data_bounds = [min(sum_values), max(sum_values)]
    curve_bounds = [-(height * amplitude_factor)/2,
                    (height * amplitude_factor)/2]
    
    # Creates the X and Y values for the point coordinates
    x_val = []
    for i in range(number_of_columns):
        x = 0
        step = width/(number_of_columns - 1)
        if i > 0:
            x = step + x_val[i - 1]
        x_val.append(x)

    y_val = []
    for value in sum_values:
        y_val.append(remap(value, data_bounds, curve_bounds))
    
    # Creates the points for interpolation based on their (X, Y) values
    # and adds them to a list of Point3d
    points = []
    for i in range(len(x_val)):
        point = r3dm.Point3d(x_val[i], y_val[i], 0)
        points.append(point)

    # Interpolates the points in a curve with start and end tangents
    # to the X-axis
    vector = r3dm.Vector3d(1, 0, 0)
    curve = Curve.CreateInterpolatedCurve2(points, 3, 2, vector, vector)
   
    # Extends the curve to guarantee that the offset curves won't
    # bulge to the inside of the art
    ext_curve = Curve.Extend2(curve, 1, width, 0)
    ext_curve = Curve.Extend2(ext_curve, 2, width, 0)

    # Creates the curve bounding box to get the center of the canvas
    bbox = r3dm.GeometryBase.GetBoundingBox(ext_curve)
    center = bbox.Center

    # Create the base surface for splitting
    normal = r3dm.Vector3d(0, 0, 1)
    pln = r3dm.Plane(center, normal)

    p1 = r3dm.Point3d(center.X - (width/2), center.Y - (height/2), 0)
    p2 = r3dm.Point3d(center.X + (width/2), center.Y - (height/2), 0)
    p3 = r3dm.Point3d(center.X + (width/2), center.Y + (height/2), 0)
    p4 = r3dm.Point3d(center.X - (width/2), center.Y + (height/2), 0)
    
    frame = r3dm.Polyline([p1, p2, p3, p4, p1])
    srf = r3dm.Brep.CreateTrimmedPlane(pln, frame.ToNurbsCurve())

    # Create all the offsets for the base curve, using the column width
    # as the offset distance
    dist = width/(number_of_columns - 1)
    number_of_offsets = 40
    split_curves = []
    active_pos = ext_curve
    active_neg = ext_curve
    for i in range(number_of_offsets):
        positive = Curve.Offset(active_pos, pln, dist, 0.1, 2)
        negative = Curve.Offset(active_neg, pln, -dist, 0.1, 2)
        split_curves.append(positive[0])
        split_curves.append(negative[0])
        active_pos = positive[0]
        active_neg = negative[0]
    
    # Create all the vertical lines that will be used for splitting the
    # surface, using the column width as its spacing factor
    i = 2
    while i < (number_of_columns - 1):
        p1 = r3dm.Point3d(x_val[i], center.Y - height/2, 0)
        p2 = r3dm.Point3d(x_val[i], center.Y + height/2, 0)
        line = r3dm.Curve.CreateControlPointCurve([p1, p2], 1)
        split_curves.append(line)
        i += 2
    
    # Splits the surface using the offset curves and vertical lines
    split_curves.append(ext_curve)
    split = Brep.Split3(srf, split_curves, 0.01)
    
    # # DEBUGGING
    # for srf in split:
    #     model.Objects.AddBrep(srf)
    # model.Objects.AddCurve(curve)
    # model.Objects.AddCurve(ext_curve)
    # model.Write('geometry.3dm')

    # Gets the face border and area centroid for each split surface
    borders = []
    centroids = []
    for brep in split:
        edges = Brep.GetWireframe(brep, 0)
        border = Curve.JoinCurves(edges)[0]
        amp = AreaMassProperties.Compute(border)['Centroid']
        centroid = r3dm.Point3d(amp['X'], amp['Y'], 0)
        borders.append(border)
        centroids.append(centroid)

    # Sorts the curves by column, from left to right
    columns = {}
    for i in range(len(x_val) - 1):
        columns[i] = []
        for j in range(len(borders)):
            if x_val[i] < centroids[j].X < x_val[i + 1]:
                columns[i].append((borders[j], centroids[j].Y))
    
    # Sorts each column from bottom to top, and updates the
    # dictionary by leaving just the curves in each key
    for col in columns.keys():
        sort = sorted(columns[col], key= lambda x:x[1])
        sorted_col = []
        for tup in sort:
            sorted_col.append(tup[0])
        columns[col] = sorted_col
    
    # Creates the color scheme lists based on the number of colors
    color_scheme = {}
    column_index = []
    for key in columns.keys():
        column_index.append(key)
    for i in range(len(colors)):
        color_scheme[i] = column_index[i::len(colors)]

    # Sorts each curve in their respective layer based on the
    # color scheme ordering
    for key in color_scheme.keys():
        for col in color_scheme[key]:
            i = 0
            color = key
            while i < len(columns[col]):
                att = r3dm.ObjectAttributes()
                att.LayerIndex = color
                model.Objects.AddCurve(columns[col][i], att)
                if color == (len(colors) - 1):
                    color = 0
                else:
                    color += 1
                i += 1

    # Saves the 3DM file after all geometric operations are completed
    model.Write('geometry.3dm')
    
    return