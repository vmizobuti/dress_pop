# make_rhino.py
#
# Functions for generating the art using RhinoScript.
# The generative system is based on a set of sound parameters.

import rhino3dm as r3dm
import compute_rhino3d.Util
import compute_rhino3d.Curve

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

    # Reads and allocates the Rhino-Compute's authentication token
    with open('authToken.txt', 'r') as file:
        token = file.read().rstrip()
    #compute_rhino3d.Util.authToken = token
    compute_rhino3d.Util.url = "http://localhost:8081/"

    # Creates the 3DM file for all geometric operations
    model = r3dm.File3dm()

    # Creates the data chunks for point coordinates
    number_of_columns = 30
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
    # and adds them to a Point3dList
    points = []
    for i in range(len(x_val)):
        point = r3dm.Point3d(x_val[i], y_val[i], 0)
        points.append(point)

    # Interpolates the points in a curve with start and end tangents
    # to the X-axis
    vector = r3dm.Vector3d(1, 0, 0)
    curve = compute_rhino3d.Curve.CreateInterpolatedCurve2(points, 3, 2,
                                                           vector, vector)
    
    ext_start = compute_rhino3d.Curve.Extend2(curve, 1, width/2, 0)
    ext_end = compute_rhino3d.Curve.Extend2(ext_start, 2, width/2, 0)

    print(type(ext_end))
    
    model.Objects.AddCurve(ext_end)

    # Saves the 3DM file after all geometric operations are completed
    model.Write('geometry.3dm')
    
    return