from typing import List

def read(data: str):
  bytes = [(x, y) for line in data.splitlines() for x, y in [map(int, line.split(','))]]
  maxY = 0
  maxX = 0
  for x,y in bytes:
    if x > maxX: maxX = x
    if y > maxY: maxY = y
  return bytes, maxX, maxY

dd = [[-1, 0], [0, 1], [1, 0], [0, -1]]
def get_next_positions(y: int, x: int, grid: List[List[int]], maxX: int, maxY: int):
  positions = []
  for dir in range(4):
    next_y = y + dd[dir][0]
    next_x = x + dd[dir][1]
    if next_y < 0 or next_y > maxY or next_x < 0 or next_x > maxX:
      continue
    if grid[next_y][next_x] == '#': continue
    positions.append((next_y, next_x))
  return positions
  

def run(data: str, isTest, *args) -> int:
  bytes, maxX, maxY = read(data)
  grid = [['.' for _ in range(maxX + 1)] for _ in range(maxY + 1)]
  for x,y in bytes[:(12 if isTest else 1024)]:
    grid[y][x] = '#'
  
  batch = [(0,0)]
  
  steps = -1
  seen = set()
  finished = False
  while batch and not finished:
    steps += 1
    next_batch = []
    for y, x in batch:
      if (y, x) in seen: continue
      seen.add((y, x))
      if y == maxX and x == maxX: finished = True
      
      positions = get_next_positions(y, x, grid, maxX, maxY)
      next_batch.extend(positions)
    batch = next_batch
  return steps