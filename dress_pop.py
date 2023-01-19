# Implementação conceitual de arte para DressPOP 
#
# Autor: Vinicius Mizobuti / Superlimão
# 
# Versão: 1.0

from gtts import gTTS
from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np

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

def plot_sound_wave(frame_rate, frame_count, duration, data):
    """
    Plots the sound wave of a given MP3 file by passing its parameters.
    """
    
    # Creates the timestamp for the audio
    timestamp = np.linspace(0, frame_count/frame_rate, num=int(frame_count))
    
    # Plots the sound wave using matplotlib functions
    plt.figure(figsize=(15, 5))
    plt.plot(timestamp, data)
    plt.title('Teste')
    plt.ylabel('Amplitude')
    plt.xlabel('Time (s)')
    plt.xlim(0, duration)
    plt.show()

def main():

    # Gets a text from the user to input in the process
    text = input("Escreva o texto que você quer transformado:")

    # Transforms the input text to speech audio
    filename = text_to_speech(text)

    # Gets the parameters from the speech audio
    parameters = get_audio_parameters(filename)

    # Splits the parameters into individual values
    fr = parameters[0]
    fc = parameters[1]
    dt = parameters[2]
    da = parameters[3]

    # Plots the sound wave given audio parameters
    plot_sound_wave(fr, fc, dt, da)

if __name__ == '__main__':
    main()