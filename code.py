# William Goethals
# Baby Synth
# July 26th 2023

import board
import digitalio
import time
import keypad
import asyncio
from audiocore import WaveFile
from audiopwmio import PWMAudioOut as AudioOut

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

audio = AudioOut(board.GP14)
path = "sounds/"

def play_sound(filename):
    with open(path + filename, "rb") as wave_file:
        wave = WaveFile(wave_file)
        audio.play(wave)
        while audio.playing:
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
                    if (pin == board.GP0):
                        play_sound("drum_loop.wav")
                        print("this was gp0")
                    elif (pin == board.GP1):
                        play_sound("ohohoh2.wav")
                        print("this was gp1")
                    elif (pin == board.GP2):
                        play_sound("amen6.wav")
                        print("this was gp2")
                    print("pin went low")
                elif event.released:
                    print("pin went high")
            await asyncio.sleep(0)

async def main():
    print("Got to main")
    interrupt_task0 = asyncio.create_task(catch_pin_transitions(board.GP0))
    interrupt_task1 = asyncio.create_task(catch_pin_transitions(board.GP1))
    interrupt_task2 = asyncio.create_task(catch_pin_transitions(board.GP2))
    await asyncio.gather(interrupt_task0, interrupt_task1, interrupt_task2)

asyncio.run(main())


