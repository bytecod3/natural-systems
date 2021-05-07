import numpy as np
import wave, math

samplingRate = 44100  # 44.1kHz
numberOfSamples = samplingRate * 5   # 5 second clip

x = np.arange(numberOfSamples) / float(samplingRate)
vals = np.sin(2.0 * math.pi * 220 * x)

data = np.array(vals*32767, 'int16').tobytes()

# write to WAV file
with wave.open('sine220.wav', 'wb') as soundFile:
    soundFile.setparams((1, 2, samplingRate, numberOfSamples, 'NONE', 'uncompressed'))
    soundFile.writeframes(data)
    soundFile.close()
