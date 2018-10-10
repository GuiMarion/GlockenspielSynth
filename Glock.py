import numpy as np
import sounddevice as sd
import time
import pygame


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


        self.params_notes = [0, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392., 415.3, 440., 466.16, 493.88]

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
                    Note(2*self.params_notes[1]).play()                 
                if event.key == pygame.K_o:
                    # do#
                    Note(2*self.params_notes[2]).play()

                if event.key == pygame.K_l:
                    # re
                    Note(2*self.params_notes[3]).play()

                if event.key == pygame.K_p:
                    # re#
                    Note(2*self.params_notes[4]).play()

                if event.key == pygame.K_m:
                    # mi
                    Note(2*self.params_notes[5]).play()


    def quit(self):
        self.playing = False
        pygame.quit()
        quit()




class Note:

    def __init__(self, params, sampleRate = 44100):
        self.sampleRate = sampleRate
        self.params = params # Parameters for the physical model

        self.length = 0.1
        # Length should be computed from the physical model


    # Temporary !!
    def getFreq(self):

        return self.params


    def getHarmonics(self):

        # TODO call the physical model to get the harmonics

        return [1]

    def getSignal(self):

        atten = 0.3
        # atten is the attenuation we want, should depend of time

        each_sample_number = np.arange(self.length * self.sampleRate)
        waveform = np.sin(2 * np.pi * each_sample_number * self.getFreq() / self.sampleRate) * atten
        

        return waveform

    def play(self):

        # Play the waveform out the speakers
        sd.play(self.getSignal(), self.sampleRate)
        time.sleep(self.length)
        sd.stop()


glock = Glockenspiel()
glock.run()


