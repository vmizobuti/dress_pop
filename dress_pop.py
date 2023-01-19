# Implementação conceitual de arte para DressPOP 
#
# Autor: Vinicius Mizobuti / Superlimão
# 
# Versão: 1.0

from gtts import gTTS
from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np

text = "Deus nos acuda"
tts = gTTS(text, lang='pt-br')
tts.save("Teste.mp3")

audio = AudioSegment.from_mp3("Teste.mp3")
frame_rate = audio.frame_rate
frame_count = audio.frame_count()
duration = audio.duration_seconds
data = audio.get_array_of_samples()

timestamp = np.linspace(0, frame_count/frame_rate, num=int(frame_count))

plt.figure(figsize=(15, 5))
plt.plot(timestamp, data)
plt.title('Teste')
plt.ylabel('Amplitude')
plt.xlabel('Time (s)')
plt.xlim(0, duration)
plt.show()