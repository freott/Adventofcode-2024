from functools import reduce
from itertools import combinations, product
import math
from pprint import pprint

SECONDS = 100

def read(data: str):
  robots = []
  for row in data.splitlines():
    robot = [
      list(map(int, val.split(','))) 
      for part in row.split(' ') 
      for val in part.split('=')[1:]
    ]
    robots.append(robot)
  return robots

def run(data: str, isTest: bool) -> int:
  WIDTH = 11 if isTest else 101
  HEIGHT = 7 if isTest else 103
  robots = read(data)
  
  destinations = []
  for [[px, py], [vx, vy]] in robots:
    new_px = (px + vx * SECONDS) % WIDTH
    new_py = (py + vy * SECONDS) % HEIGHT
    destinations.append((new_px, new_py))
    
  quadrant_results = []
  for y_part, x_part in product(range(2), range(2)):
    x_min = x_part * math.ceil(WIDTH / 2)
    x_max = math.floor((x_part + 1) * WIDTH / 2) - 1
    y_min = y_part * math.ceil(HEIGHT / 2)
    y_max = math.floor((y_part + 1) * HEIGHT / 2) - 1
    count = 0
    for x, y in destinations:
      if x_min <= x <= x_max and y_min <= y <= y_max: 
        count += 1
    quadrant_results.append(count)
    
  return reduce(lambda a, b: a * b, quadrant_results) 