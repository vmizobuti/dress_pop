from gtts import gTTS
from pydub import AudioSegment
from os import remove

def text_to_speech(text):
    """
    Transforms an input text into an MP3 file.
    """
    
    # Transforms a text into an MP3 file using gtts
    tts = gTTS(text, lang='pt-br')

    # Saves the file in the current directory given a filename
    filename = text + ".mp3"
    tts.save(filename)

    return filename

def get_audio_parameters(filepath):
    """
    Gets all sound parameters from a given MP3 file.
    """
    
    # Reads the MP3 file using pydub
    audio = AudioSegment.from_mp3(filepath)

    # Gets the frame rate, frame count, duration and samples
    # from a given file
    frame_rate = audio.frame_rate
    frame_count = audio.frame_count()
    duration = audio.duration_seconds
    data = audio.get_array_of_samples()

    return frame_rate, frame_count, duration, data

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

def hsl_to_rgb(color):
    """
    Converts an HSL color to the RGB space.
    This function derives from the algorithm found at:
    https://www.baeldung.com/cs/convert-color-hsl-rgb
    """
    
    # Adjusts negative hues to their positive values
    if color[0] < 0:
        color[0] = 360 + color[0]

    # Computes the chroma value
    chroma = (1 - abs(2*color[2] - 1)) * color[1]

    # Searches for an (R, G, B) point with the same hue and chroma
    # of the input color
    rgb_point = []
    h_prime = color[0] / 60
    x = chroma * (1 - abs((h_prime % 2) - 1))

    if 0 <= h_prime < 1:
        rgb_point = [chroma, x, 0]
    elif 1 <= h_prime < 2:
        rgb_point = [x, chroma, 0]
    elif 2 <= h_prime < 3:
        rgb_point = [0, chroma, x]
    elif 3 <= h_prime < 4:
        rgb_point = [0, x, chroma]
    elif 4 <= h_prime < 5:
        rgb_point = [x, 0, chroma]
    elif 5 <= h_prime <= 6:
        rgb_point = [chroma, 0, x]
    
    # Computes the lightness of the RGB color
    m = color[2] - (chroma/2)

    # Computes the final RGB color by adding m to each RGB point
    rgb_color = [round((rgb_point[0] + m) * 255),
                 round((rgb_point[1] + m) * 255),
                 round((rgb_point[2] + m) * 255)]
    
    return rgb_color

def make_colors(text, saturation, scheme):
    """
    Creates a list of RGB colors based on the audio of a text.
    The saturation level of those colors are decided by the user.
    """

    # Transforms the input text to speech audio
    filename = text_to_speech(text)

    # Gets the parameters from the speech audio and deletes the file
    parameters = get_audio_parameters(filename)
    remove(filename)

    # Removes all negative values from the dataset, assuming that the
    # audio levels have some kind of symmetry
    data = []
    for value in parameters[3]:
        if value > 0:
            data.append(value)

    # Divides the sound into chunks of data. Each chunk will represent
    # a color later in the process
    number_of_chunks = 5
    chunk_size = round(len(data)/number_of_chunks)
    partitions = [data[i:i + chunk_size] for i in \
                  range(0, len(data), chunk_size)]

    # Process the chunks of data into their mean and max values,
    # the means will be used to compute the hue while the max
    # values of each chunk will define its lightness
    list_of_means = []
    list_of_max = []

    for partition in partitions:
        mean_value = round(sum(partition)/len(partition))
        max_value = max(partition)

        list_of_means.append(mean_value)
        list_of_max.append(max_value)
    
    mean_bounds = [min(list_of_means), max(list_of_means)] 
    max_bounds = [min(list_of_max), max(list_of_max)]  
    
    # Defines the hue bounds based on the color scheme from the user input
    hue_bounds = []
    if scheme == 'Vermelhos':
        hue_bounds = [-75, 15]
    elif scheme == 'Verdes':
        hue_bounds = [75, 150]
    elif scheme == 'Azuis':
        hue_bounds = [180, 240]
    elif scheme == 'Mix':
        hue_bounds = [-120, 60]
    
    # Remaps the mean values to their respective hue value
    hue = []
    for mean in list_of_means:
        hue_value = round(remap(mean, mean_bounds, hue_bounds))
        hue.append(hue_value)
    
    # Remaps the max values to their respective lightness value
    light_bounds = [0.3, 0.8]
    lightness = []

    for value in list_of_max:
        max_value = round(remap(value, max_bounds, light_bounds), 3)
        lightness.append(max_value)
    
    # Composes the HSL color given a hue, saturation and lightness value
    hsl_colors = []
    for i in range(number_of_chunks):
        color = [hue[i], saturation, lightness[i]]
        hsl_colors.append(color)

    # Translates the HSL color to RGB space
    rgb_colors = []
    for color in hsl_colors:
        rgb_color = hsl_to_rgb(color)
        rgb_colors.append(rgb_color)
    
    # Remove the last color from the list, that is typically Black
    # due to the fading of  the audio, and add White to the extremes
    rgb_colors.pop(len(rgb_colors) - 1)

    return rgb_colors