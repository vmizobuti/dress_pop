# make_rhino.py
#
# Functions for generating the art using RhinoScript.
# The generative system is based on a set of sound parameters.

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

    # Creates the data chunks for point coordinates
    number_of_columns = 15
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
    
    return