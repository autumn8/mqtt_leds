from time import sleep
import board
import neopixel
pixels = neopixel.NeoPixel(board.D18, 30)
pixels[0] = (255, 255, 255)

def on(color, brightness=1):
  pixels.brightness=brightness
  pixels.fill(color)

def off():
 pixels.fill((0,0,0))

def strobe(color, interval, duration):
  counter=0
  while True:
    if counter %2 ==0:
      pixels.fill(color)
    else:
      pixels.fill((0,0,0))
    counter+=1
    sleep(interval)

#strobe(color=(255,255,255), interval=0.5, duration=30)
off() 
#on((255,147,41), 0.2)
