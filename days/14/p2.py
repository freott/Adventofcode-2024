from itertools import combinations, product
import math
from pprint import pprint

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
  seconds = -1
  while (True):
    seconds += 1
    destinations = set()
    continue_while = False
    for [[px, py], [vx, vy]] in robots:
      new_px = (px + vx * seconds) % WIDTH
      new_py = (py + vy * seconds) % HEIGHT
      destination = (new_px, new_py)
      if (destination in destinations): 
        continue_while = True
        break
      destinations.add((new_px, new_py))
    
    if continue_while: continue
    
    grid = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for x, y in destinations:
      grid[y][x] = '#'
      
    print(f'\nAfter {seconds} seconds:')
    for row in grid:
      print(" ".join(row))
    else:
      print("View already seen")
    input("Press Enter to continue...")