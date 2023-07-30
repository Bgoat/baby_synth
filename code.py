# William Goethals
# Baby Synth
# July 26th 2023

import board
import digitalio
# import time
import keypad
import asyncio
from audiocore import WaveFile
from audiopwmio import PWMAudioOut as AudioOut

# added for i2s
import array
import math
import audiocore
import audiobusio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

audio = AudioOut(board.GP14)
path = "sounds/"

audio2 = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2)

tone_volume = 0.1  # Increase this to increase the volume of the tone.
frequency = 440  # Set this to the Hz of the tone you want to generate.
length = 8000 // frequency
sine_wave = array.array("h", [0] * length)
for i in range(length):
    sine_wave[i] = int((math.sin(math.pi*2*i/length)) * tone_volume*(2 ** 15 - 1))
sine_wave_sample = audiocore.RawSample(sine_wave)

def play_sine(freq):
    tone_volume = 0.1  # Increase this to increase the volume of the tone.
    frequency = freq  # Set this to the Hz of the tone you want to generate.
    length = 8000 // frequency
    sine_wave = array.array("h", [0] * length)
    for i in range(length):
        sine_wave[i] = int((math.sin(math.pi*2*i/length)) * tone_volume*(2 ** 15 - 1))
    sine_wave_sample = audiocore.RawSample(sine_wave)
    audio2.play(sine_wave_sample, loop=True)
    
    
def play_sound(filename):
    with open(path + filename, "rb") as wave_file:
        wave = WaveFile(wave_file)
        audio2.play(wave)
        while audio2.playing:
            pass

# while True:
#    led.value = True
#    time.sleep(0.1)
#    play_sound("drum_loop.wav")
#    led.value = False
#    time.sleep(0.5)

async def catch_pin_transitions(pin):
    with keypad.Keys((pin,), value_when_pressed=False) as keys:
        while True:
            event = keys.events.get()
            if event:
                if event.pressed:
                    if (pin == board.GP3):
                        # play_sound("drum_loop.wav")
                        print("this was gp3")
                        play_sine(500)
                        # audio2.play(sine_wave_sample, loop=True)
                    elif (pin == board.GP4):
                        # play_sound("ohohoh2.wav")
                        play_sine(1000)
                        print("this was gp4")
                    elif (pin == board.GP5):
                        # play_sound("amen6.wav")
                        play_sine(2000)
                        print("this was gp5")
                    print("pin went low")
                elif event.released:
                    print("pin went high")
            await asyncio.sleep(0)

async def main():
    print("Got to main")
    interrupt_task0 = asyncio.create_task(catch_pin_transitions(board.GP3))
    interrupt_task1 = asyncio.create_task(catch_pin_transitions(board.GP4))
    interrupt_task2 = asyncio.create_task(catch_pin_transitions(board.GP5))
    await asyncio.gather(interrupt_task0, interrupt_task1, interrupt_task2)

asyncio.run(main())


