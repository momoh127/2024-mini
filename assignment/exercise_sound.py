#!/usr/bin/env python3
"""
PWM Tone Generator

based on https://www.coderdojotc.org/micropython/sound/04-play-scale/
"""

import machine
import utime

# GP16 is the speaker pin
SPEAKER_PIN = 16

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))


def playtone(frequency: float, duration: float) -> None:
    speaker.duty_u16(1000)
    speaker.freq(frequency)
    utime.sleep(duration)
    quiet()


def quiet():
    speaker.duty_u16(0)

C = 523
E = 659
G = 784

mario_song = [ (E, 0.2), (E, 0.2), (0, 0.1), (E, 0.2), (0, 0.1), 
              (C, 0.2), (E, 0.2), (G, 0.4)]

for note, duration in mario_song:
    if note == 0:
        quiet()
    else:
        playtone(note, duration)
    utime.sleep(0.05)

# Turn off the PWM
quiet()
