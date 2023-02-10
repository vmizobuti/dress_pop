import matplotlib.pyplot as plt
import numpy as np

def plot_sound_wave(frame_rate, frame_count, duration, data, title):
    """
    Plots the sound wave of a given MP3 file by passing its parameters.
    """
    
    # Creates the timestamp for the audio
    timestamp = np.linspace(0, frame_count/frame_rate, num=int(frame_count))
    
    # Plots the sound wave using matplotlib functions
    plt.figure(figsize=(15, 5))
    plt.plot(timestamp, data, linewidth=0.1)
    plt.title(title)
    plt.ylabel('Amplitude')
    plt.xlabel('Time (s)')
    plt.xlim(0, duration)
    plt.show()