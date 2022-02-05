import os
import scipy.io
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt

myAudioFilename = 'sound.wav'  #  plot this wav file     ~/audio/aaa.wav

dataset_path = os.path.join("D:/CODE/BEAR/BEAR/sounds") # homedir -> audiodir -> my wav files
wavedata = os.path.join(dataset_path, myAudioFilename)
   
sampleRate, audioBuffer = scipy.io.wavfile.read(wavedata)

duration = len(audioBuffer)/sampleRate

time = np.arange(0,duration,1/sampleRate) #time vector

plt.plot(time,audioBuffer)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title(myAudioFilename)
plt.show()