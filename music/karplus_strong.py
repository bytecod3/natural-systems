import argparse
import os
import random
import time
import wave
from collections import deque

import numpy as np
import pygame
from matplotlib import pyplot as plt

# show plot of algorithm in action?
gShowPlot = False

# notes of a Pentatonic Minor scale
# piano C4-E(b)-F-G-B(b)-C5
pmNotes = {'C4': 262, 'Eb': 311, 'F': 349, 'G': 391, 'Bb': 466}


def writeWaveFile(fname, data):
    with wave.open(fname, 'wb') as file:
        nChannels = 1  # single channel
        sampleWidth = 2  # 16-bit
        frameRate = 44100
        nFrames = 44100  # which means its a 1-second sample

        # set parameters
        file.setparams((nChannels, sampleWidth, frameRate, nFrames, 'NONE', 'uncompressed'))
        file.writeframes(data)
        file.close()


# generate a note of a given frequency
def generateNote(frequency):
    nSamples = 44100
    sampleRate = 44100
    N = int(sampleRate / frequency)

    # initialize the ring buffer
    buf = deque([random.random() - 0.5 for i in range(N)])

    # plot if flag set
    if gShowPlot is True:
        axline, = plt.plot(buf)

    # initialize samples buffer (We are using a ring buffer here for efficiency. Time complexity = O(1) )
    samples = np.array([0] * nSamples, 'float32')

    for i in range(nSamples):
        samples[i] = buf[0]
        average = 0.995 * 0.5 * (buf[0] + buf[1])  # this right here implements the KS Low Pass Filter
        buf.append(average)
        buf.popleft()

        # plot if flag set
        if gShowPlot:
            if i % 1000 == 0:
                axline.set_ydata(buf)
                plt.draw()

    # convert samples to 16-bit values and then to a string
    # the maximum value for 16-bit is 32767
    samples = np.array(samples * 32767, 'int16')

    # we finally return the decayed (filtered) array. This represents the decay of the fundamental note as the string
    # gets damped

    return samples.tobytes()


class NotePlayer:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)  # 2048 gives the buffer size
        pygame.init()

        # dictionary of notes
        self.notes = {}

    # add note
    def add(self, fileName):
        self.notes[fileName] = pygame.mixer.Sound(fileName)

    # play a note
    def play(self, fileName):
        try:
            self.notes[fileName].play()
        except:
            print("[-]" + fileName + " not found!")

    # play a random note
    def playRandom(self):
        index = random.randint(0, len(self.notes) - 1)
        note = list(self.notes.values())[index]
        note.play()


def main():
    # declare global var
    global gShowPlot

    parser = argparse.ArgumentParser(description="Generating sounds with Karplus-Strong algorithm")

    # add arguments
    parser.add_argument('--display', action='store_true', required=False)
    parser.add_argument('--play', action='store_true', required=False)
    parser.add_argument('--piano', action='store_true', required=False)
    args = parser.parse_args()

    print(args)

    # show plot if flag set
    # if args.display:
        # gShowPlot = True
        # plt.ion()

    # # create Note player
    # nplayer = NotePlayer()
    #
    # print('Creating notes...')
    # for name, freq in list(pmNotes.items()):
    #     fileName = name + '.wav'
    #     if not os.path.exists(fileName) or args.display:
    #         data = generateNote(freq)
    #         print('Creating ' + fileName + '...')
    #         writeWaveFile(fileName, data)
    #     else:
    #         print(fileName + ' already created. Skipping...')
    #
    #     # add note to player
    #     nplayer.add(name + '.wav')
    #
    #     # play note if display flag set
    #     if args.display:
    #         nplayer.play(name + '.wav')
    #         time.sleep(0.5)
    #
    # # play a random tune
    # if args.play:
    #     while True:
    #         try:
    #             nplayer.playRandom()
    #             # rest - 1 to 8 beats
    #             rest = np.random.choice([1, 2, 4, 8], 1, p=[0.15, 0.7, 0.1,
    #                                                         0.05])  # 2 beat break has the highest probability of
    #             # being selected
    #             time.sleep(0.25 * rest[0])
    #
    #         except KeyboardInterrupt:
    #             exit()
    #
    # # random piano mode
    # if args.play:
    #     while True:
    #         for event in pygame.event.get():
    #             if event.type == pygame.KEYUP:
    #                 print("key pressed")
    #                 nplayer.playRandom()
    #                 time.sleep(0.5)


if __name__ == '__main__':
    main()
