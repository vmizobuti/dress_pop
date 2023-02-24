# make_sound.py
#
# Functions for generating a sound based on a text
# and returning its wave parameters.

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

def sound_parameters(text):
    """
    Gets all sound parameters from a given MP3 file.
    """

    # Makes the MP3 file based on a given text and returns its filepath
    filepath = text_to_speech(text)

    # Reads the MP3 file using pydub
    audio = AudioSegment.from_mp3(filepath)

    # Gets the frame rate, frame count, duration and samples
    # from a given file
    frame_rate = audio.frame_rate
    frame_count = audio.frame_count()
    duration = audio.duration_seconds
    data = audio.get_array_of_samples()

    # Deletes the MP3 file after using it
    remove(filepath)

    return frame_rate, frame_count, duration, data
