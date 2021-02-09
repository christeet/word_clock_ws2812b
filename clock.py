#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import *
import argparse
import datetime

# LED strip configuration:
LED_COUNT      = 114      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 55     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

LAST_MINUTE_ENTRY = 0

AS_ISCH = [109, 108, 106, 105, 104, 103]
M_FUF = [101, 100, 99]
M_ZAA = [96, 97, 98]
M_VIERTU = [88, 89, 90, 91, 92, 93]
M_ZWANZG = [87, 86, 85, 84, 83, 82]
VOR = [79, 78, 77]
AB = [66, 67]
M_HAUBI = [69, 70, 71, 72, 73]
EUFI = [15, 14, 13, 12]
FUFI = [50, 51, 52, 53]
EIS = [65, 64, 63]
ZWOI = [62, 61, 60, 59]
DRU = [57, 56, 55]
VIERI = [44, 45, 46, 47, 48]
SACHSI = [43, 42, 41, 40, 39, 38]
ACHTI = [22, 23, 24, 25, 26]
SIBNI = [37, 36, 35, 34, 33]
ZWOUFI = [3, 4, 5, 6, 7, 8]
ZANI = [21, 20, 19, 18]
NUNI = [28, 29, 30, 31]

# rosa 250,9,251
# blauviolette 25,9,251
# dunkelviolette 119,62,255

def drawMatrix(strip):
  time_has_changed(True)
  array = create_time_array(strip)
  display_array(strip, Color(255,255,255), array)

  while True:
    array = create_time_array(strip)
    display_array(strip, Color(255,255,255), array, True)
    time.sleep(10)


def display_array(strip, color, array, rainbow = False):
  rgbs = generate_gradient_rgbs(len(array)+1)
  j = 0
  for i in range(strip.numPixels()):
    if array.__contains__(i):
      if rainbow == True:
        strip.setPixelColor(i, Color(int(rgbs[j][0]), int(rgbs[j][1]), int(rgbs[j][2])))
        j += 1
      else:
        strip.setPixelColor(i, color)
    else:
      strip.setPixelColor(i, Color(0,0,0))
  strip.show()

def create_time_array(strip):
  now = datetime.datetime.now()
  hour = now.hour
  time_array = []
  min = LAST_MINUTE_ENTRY
  if time_has_changed(False) == True:
    # if hour == 7 and min == 00 or hour == 15 and min == 10:
    if min == 45:
      rainbow(strip)
    if min == 55:
      theaterChase(strip, Color(127,127,127), 50, 30)
  time_array = time_array + AS_ISCH + minutes(now.minute) + minutes_4(now.minute)
  # print("hour: ", hour)
  if now.minute <= 24:
    time_array = time_array + hours(hour)
  else:
    time_array = time_array + hours(hour + 1)
  # print("Time array: ", time_array)
  return time_array

def minutes(now_minute):
  # print("Real minutes: " + str(now_minute))
  if now_minute >= 5 and now_minute < 10:
    return M_FUF + AB
  elif now_minute >= 10 and now_minute < 15:
    return M_ZAA + AB
  elif now_minute >= 15 and now_minute < 20:
    return M_VIERTU + AB
  elif now_minute >= 20 and now_minute < 25:
    return M_ZWANZG + AB
  elif now_minute >= 25 and now_minute < 30:
    return M_FUF + VOR + M_HAUBI
  elif now_minute >= 30 and now_minute < 35:
    return M_HAUBI
  elif now_minute >= 35 and now_minute < 40:
    return M_FUF + AB + M_HAUBI
  elif now_minute >= 40 and now_minute < 45:
    return M_ZWANZG + VOR
  elif now_minute >= 45 and now_minute < 50:
    return M_VIERTU + VOR
  elif now_minute >= 50 and now_minute < 55:
    return M_ZAA + VOR
  elif now_minute >= 55 and now_minute <= 59:
    return M_FUF + VOR
  else:
    return []

def minutes_4(now_minute):
  count = now_minute % 5
  # print("Minute: " + str(count))
  if count == 1:
    return [110]
  if count == 2:
    return [110,111]
  if count == 3:
    return [110,111,112]
  if count == 4:
    return [110,111,112,113]
  if count == 0:
    return []

def hours(next_hour):
  if next_hour == 1 or next_hour == 13:
    return EIS
  if next_hour == 2 or next_hour == 14:
    return ZWOI
  if next_hour == 3 or next_hour == 15:
    return DRU
  if next_hour == 4 or next_hour == 16:
    return VIERI
  if next_hour == 5 or next_hour == 17:
    return FUFI
  if next_hour == 6 or next_hour == 18:
    return SACHSI
  if next_hour == 7 or next_hour == 19:
    return SIBNI
  if next_hour == 8 or next_hour == 20:
    return ACHTI
  if next_hour == 9 or next_hour == 21:
    return NUNI
  if next_hour == 10 or next_hour == 22:
    return ZANI
  if next_hour == 11 or next_hour == 23:
    return EUFI
  if next_hour == 12 or next_hour == 00 or next_hour == 24:
    return ZWOUFI

def generate_gradient_rgbs(num_buckets):
  rgb_codes = []
  step_size = 1024 / num_buckets
  for step in range(0,num_buckets):
    red = int(max(0, 255 - (step_size*step*0.5)))
    blue = int(max(0, 255 - (step_size*0.5*(num_buckets-step-1))))
    green = (255 - red) if red else (255 - blue)
    rgb_codes.append((red, green, blue))
  return rgb_codes

def rainbow(strip, wait_ms=20, iterations=1):
  for j in range(2*iterations):
    for i in range(strip.numPixels()):
      strip.setPixelColor(i, wheel((i*j) & 255))
      strip.show()
      time.sleep(wait_ms/1000.0)

def wheel(pos):
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(5/100)
        strip.setPixelColor(i, Color(0,0,0))
        strip.show()

def wipeStrip(strip, color, wait_ms=5):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000)

def time_has_changed(isStartup):
    global LAST_MINUTE_ENTRY
    now = datetime.datetime.now()
    if isStartup == True:
        LAST_MINUTE_ENTRY = round(now.minute / 5) * 5 #round to nearest five
        return True
    if LAST_MINUTE_ENTRY != now.minute:
        if now.minute % 5 == 0:
            LAST_MINUTE_ENTRY = now.minute
            return True
    return False

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
  args = parser.parse_args()

  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  strip.begin()

  print ('Press Ctrl-C to quit.')
  if not args.clear:
    print('Use "-c" argument to clear LEDs on exit')

  try:
    drawMatrix(strip)
  except KeyboardInterrupt:
    if args.clear:
      wipeStrip(strip, Color(0,0,0), 10)
