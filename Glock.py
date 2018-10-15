import numpy as np
import sounddevice as sd
import time
import pygame
from threading import Thread
import math
import matplotlib.pyplot as plt

SAMPLE_RATE = 44100

class Bar:

    def __init__(self, L, l, h, ro, E):
        self.L = L
        self.l = l 
        self.ro = ro
        self.h = h
        self. V = l * L * h
        self.S = l * h 
        self. M = ro * self.V
        #self.I = 1/12 * ro * h * l * L**3
        self.I = 1/12 * self.M * L**2
        self.E = E

        self.length = 1
        self.atten = 0.6
        self.tau = 10**-6

    def getFreq(self, n):

        return 1/1000 * math.sqrt(self.E*self.I/(self.ro*self.S))*(math.pi/(8*self.L**2))*((2*n)+1)**2

    def getFreqs(self):

        F = []
        f = self.getFreq(1)
        n = 1
        while f < 30000:
            F.append(f)
            f = self.getFreq(n)        
            n += 1

        return F

    def add(self, L, L2):
        if len(L) == len(L2):
            for i in range(len(L)):
                L[i] += L[i]
            return L
        else:
            raise ValueError("List must have same size")


    def getSignal(self):

        F = self.getFreqs()

        each_sample_number = np.arange(self.length * SAMPLE_RATE)

        atten = self.atten

        S = np.sin(2 * np.pi * each_sample_number * self.getFreq(1) / SAMPLE_RATE)

        for i in range(len(S)):
            S[i] = S[i] * math.exp(-i*self.getFreq(1)*self.tau)

        for freq in F[1:]:

            tau = freq*self.tau

            s = np.sin(2 * np.pi * each_sample_number * freq / SAMPLE_RATE) * atten

            for i in range(len(s)):
                s[i] = s[i] * math.exp(-i*tau)

            S = self.add(S, s)


        #plt.plot(S)
        #plt.show()

        return S

class Glockenspiel:

    def __init__(self, sampleRate = 44100):

        self.sampleRate = sampleRate

        # SETTINGS

        WIDTH = 200
        HEIGHT = 200
        TITLE = 'Glockenspiel Synthésizer'

        #colors
        WHITE = (0,0,0)
        BLACK = (255,255,255)
        RED = (255,0,0)
        GREEN = (0,255,0)
        BLUE = (0,0,255)
        windowSize = (WIDTH,HEIGHT)

        pygame.init()

        screen = pygame.display.set_mode(windowSize)

        self.L = [0, 101, 96, 92, 87, 85, 80, 76, 72, 70, 65, 62, 60]

        self.params_notes = [(x*10**-3, 20*10**-3, 2*10**-3, 7500, 210*10**9) for x in self.L]

       #self.params_notes = [0, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392., 415.3, 440., 466.16, 493.88]

    def run(self):

        self.playing = True
        while self.playing:
            self.events()

    def events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                # Handle Key events 
                if event.key == pygame.K_ESCAPE:
                    self.quit()

                if event.key == pygame.K_q:
                    # do
                    Note(self.params_notes[1]).play()

                if event.key == pygame.K_z:
                    # do#
                    Note(self.params_notes[2]).play()

                if event.key == pygame.K_s:
                    # re
                    Note(self.params_notes[3]).play()

                if event.key == pygame.K_e:
                    # re#
                    Note(self.params_notes[4]).play()

                if event.key == pygame.K_d:
                    # mi
                    Note(self.params_notes[5]).play()

                if event.key == pygame.K_f:
                    # fa
                    Note(self.params_notes[6]).play()
                    
                if event.key == pygame.K_t:
                    # fa#
                    Note(self.params_notes[7]).play()

                if event.key == pygame.K_g:
                    # sol
                    Note(self.params_notes[8]).play()

                if event.key == pygame.K_y:
                    # sol#
                    Note(self.params_notes[9]).play()

                if event.key == pygame.K_h:
                    # la
                    Note(self.params_notes[10]).play()

                if event.key == pygame.K_u:
                    # la#
                    Note(self.params_notes[11]).play()

                if event.key == pygame.K_j:
                    # si
                    Note(self.params_notes[12]).play()

                if event.key == pygame.K_k:
                    # do
                    Note(self.params_notes[1], 2).play()                 
                if event.key == pygame.K_o:
                    # do#
                    Note(self.params_notes[2], 2).play()

                if event.key == pygame.K_l:
                    # re
                    Note(self.params_notes[3], 2).play()

                if event.key == pygame.K_p:
                    # re#
                    Note(self.params_notes[4], 2).play()

                if event.key == pygame.K_m:
                    # mi
                    Note(self.params_notes[5], 2).play()


    def quit(self):
        self.playing = False
        pygame.quit()
        quit()




class Note():

    def __init__(self, params, mult = 1):
        (self.L, self.l, self.h, self.ro, self.E) = params # Parameters of the physical model
        self.L = self.L  /mult
        self.length = 0.1
        # Length should be computed from the physical model


    def getSignal(self):

        b = Bar(self.L, self.l, self.h, self.ro, self.E)
        return b.getSignal()

    def play(self):

        # Play the waveform out the speakers
        sd.play(self.getSignal(), SAMPLE_RATE)
        time.sleep(self.length)
        sd.stop()


glock = Glockenspiel()
glock.run()


