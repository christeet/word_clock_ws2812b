#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
import argparse
import time
import datetime
from datetime import datetime

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

AS_ISCH = [[0,7], [0,6], [0,4], [0,3], [0,2], [0,1]]
M_FUF = [[1,7], [1,6], [1,5]]
M_ZAH = [[1,3], [1,2], [1,1]]
M_VIARTU = [[2,7], [2,6], [2,5], [2,4], [2,3], [2,2]]
M_ZWANZG = [[3,7], [3,6], [3,5], [3,4], [3,3], [3,2]]
AB = [[3,0], [3,1]]
VOR = [[4,7], [4,6], [4,5]]
M_HAUBI = [[5,4], [5,3], [5,2], [5,1], [5,0]]
EIS = [[6,7], [6,6], [6,5]]
ZWOI = [[6,3], [6,2], [6,1], [6,0]]
DRU = [[7,7], [7,6], [7,5]]
VIERI = [[7,4], [7,3], [7,2], [7,1], [7,0]]
FUFI = [[8,7], [8,6], [8,5], [8,4]]
SACHSI = [[9,5], [9,4], [9,3], [9,2], [9,1], [9,0]]
SIBNI = [[10,7], [10,6], [10,5], [10,4], [10,3]]
ACHTI = [[11,6], [11,5], [11,4], [11,3], [11,2]]
NUNI = [[12,7], [12,6], [12,5], [12,4]]
ZAHNI = [[13,4], [13,3], [13,2], [13,1], [13,0]]
EUFI = [[14,7], [14,6], [14,5], [14,4]]
ZWOUFI = [[15,5], [15,4], [15,3], [15,2], [15,1], [15,0]]


def demo(n, block_orientation, rotate):
  # create matrix device
  serial = spi(port=0, device=0, gpio=noop())
  device = max7219(serial, cascaded=n or 1,  block_orientation=block_orientation, rotate=rotate or 0)
  print("Created device")

  while True:
    print("Create Time Array")
    x_y_values = []
    x_y_values = choose_time_array(x_y_values)
    print("Time Array created!: ", x_y_values)
    with canvas(device) as draw:
      for x, y in x_y_values:
        draw.point((x,y), fill="red")

    time.sleep(10)

def choose_time_array(x_y_values):
  x_y_values.extend(AS_ISCH)
  parsed_time = str(datetime.now())
  hour, minute = parsed_time.split(" ")[1].split(".")[0].split(":")[:-1]
  print("Hour: ", hour)
  print("Minute: ", minute)
  next_hour = ""
  x_y_minutes, next_hour = minutes(hour, minute, x_y_values)
  x_y_full = hours(next_hour, x_y_minutes)
  print(x_y_full)
  return x_y_full

def minutes(next_hour, minute, x_y_values):
  if int(minute) >= 5 and int(minute) < 10:
    x_y_values.extend(M_FUF)
    x_y_values.extend(AB)
  elif int(minute) >= 10 and int(minute) < 15:
    x_y_values.extend(M_ZAH)
    x_y_values.extend(AB)
  elif int(minute) >= 15 and int(minute) < 20:
    x_y_values.extend(M_VIARTU)
    x_y_values.extend(AB)
  elif int(minute) >= 20 and int(minute) < 25:
    x_y_values.extend(M_ZWANZG)
    x_y_values.extend(AB)
  elif int(minute) >= 25 and int(minute) < 30:
    x_y_values.extend(M_FUF)
    x_y_values.extend(VOR)
    x_y_values.extend(M_HAUBI)
    next_hour = str(int(next_hour) + 1)
  elif int(minute) >= 30 and int(minute) < 35:
    x_y_values.extend(M_HAUBI)
    next_hour = str(int(next_hour) + 1)
  elif int(minute) >= 35 and int(minute) < 40:
    x_y_values.extend(M_FUF)
    x_y_values.extend(AB)
    x_y_values.extend(M_HAUBI)
    next_hour = str(int(next_hour) + 1)
  elif int(minute) >= 40 and int(minute) < 45:
    x_y_values.extend(M_ZWANZG)
    x_y_values.extend(VOR)
    next_hour = str(int(next_hour) + 1)
  elif int(minute) >= 45 and int(minute) < 50:
    x_y_values.extend(M_VIARTU)
    x_y_values.extend(VOR)
    next_hour = str(int(next_hour) + 1)
  elif int(minute) >= 50 and int(minute) < 55:
    x_y_values.extend(M_ZAH)
    x_y_values.extend(VOR)
    next_hour = str(int(next_hour) + 1)
  elif int(minute) >= 55 and int(minute) < 60:
    x_y_values.extend(M_FUF)
    x_y_values.extend(VOR)
    next_hour = str(int(next_hour) + 1)
  return x_y_values, next_hour

def hours(next_hour, x_y_values):
  if next_hour == "01" or next_hour == "13":
    x_y_values.extend(EIS)
  if next_hour == "02" or next_hour == "14":
    x_y_values.extend(ZWOI)
  if next_hour == "03" or next_hour == "15":
    x_y_values.extend(DRU)
  if next_hour == "04" or next_hour == "16":
    x_y_values.extend(VIARI)
  if next_hour == "05" or next_hour == "17":
    x_y_values.extend(FUFI)
  if next_hour == "06" or next_hour == "18":
    x_y_values.extend(SACHSI)
  if next_hour == "07" or next_hour == "19":
    x_y_values.extend(SIBNI)
  if next_hour == "08" or next_hour == "20":
    x_y_values.extend(ACHTI)
  if next_hour == "09" or next_hour == "21":
    x_y_values.extend(NUNI)
  if next_hour == "10" or next_hour == "22":
    x_y_values.extend(ZAHNI)
  if next_hour == "11" or next_hour == "23":
    x_y_values.extend(EUFI)
  if next_hour == "12" or next_hour == "00":
    x_y_values.extend(ZWOUFI)
  return x_y_values

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='matrix_demo arguments',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')
  parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
  parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')

  args = parser.parse_args()

  try:
    demo(args.cascaded, args.block_orientation, args.rotate)
  except KeyboardInterrupt:
    pass
