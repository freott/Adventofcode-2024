from itertools import groupby
from pprint import pprint
from typing import List, Optional
from tqdm import tqdm


def print_grid(grid, render_cell):
  print("   ", end="")
  for col in range(len(grid[0])):
    print(col, end=" " if col > 9 else "  ")
  print()
  for i, row in enumerate(grid):
    print(i, end=" " if i > 9 else "  ")
    for cell in row:
      print(render_cell(cell), end="  ")
    print()

def read(data: str):
  grid: List[List[str]] = []
  start = None
  end = None
  for y, row in enumerate(data.splitlines()):
    grid.append([])
    for x, value in enumerate(row):
      grid[y].append(value)
      if value == 'S': start = (y, x)
      if value == 'E': end = (y, x)
      
  return grid, start, end

def in_grid(y: int, x: int, grid: List[List[int]], values: Optional[List[str]] = None):
  return 0 <= y < len(grid) and 0 <= x < len(grid[0]) and (values is None or grid[y][x] in values)

def get_cheats(grid):
  cheats = []
  for y, row in enumerate(grid):
    for x, value in enumerate(row):
      if value != "#": continue
      if sum([in_grid(y, sx, grid, ['.', 'S', 'E']) for sx in [x - 1, x + 1]]) == 2: 
        cheats.append((y, x))
      elif sum([in_grid(sy, x, grid, ['.', 'S', 'E']) for sy in [y - 1, y + 1]]) == 2: 
        cheats.append((y, x))
  return cheats

dd = [[-1, 0], [0, 1], [1, 0], [0, -1]]
def get_next_positions(y: int, x: int, grid: List[List[int]]):
  positions = []
  for dir in range(4):
    next_y = y + dd[dir][0]
    next_x = x + dd[dir][1]
    if not in_grid(next_y, next_x, grid): continue
    if grid[next_y][next_x] == '#': continue
    positions.append((next_y, next_x))
  return positions

def count_seconds(grid, start, end, max_steps):
  batch = [start]
  
  steps = -1
  seen = set()
  finished = False
  while batch and not finished and steps != max_steps:
    steps += 1
    next_batch = []
    for y, x in batch:
      if (y, x) in seen: continue
      seen.add((y, x))
      if (y, x) == end: finished = True
      
      positions = get_next_positions(y, x, grid)
      next_batch.extend(positions)
    batch = next_batch
  return steps
  

def run(data: str, *args) -> int:
  grid, start, end = read(data)
  # print_grid(grid, lambda v: ' ' if v == '.' else v)
  cheats = get_cheats(grid)
  original_time = count_seconds(grid, start, end, float('inf'))
  print(original_time)
  cheat_times = []
  for i, (cheat_y, cheat_x) in tqdm(enumerate(cheats)):
    # print(f'Iteration {i} of {len(cheats)}')
    copied_grid = [row[:] for row in grid]
    copied_grid[cheat_y][cheat_x] = '.'
    time = count_seconds(copied_grid, start, end, original_time - 99)
    cheat_times.append([(cheat_y, cheat_x), original_time - time])
  cheat_times = sorted(cheat_times, key=lambda x: x[1])
  grouped_times = groupby(cheat_times, key=lambda x: x[1])
  # pprint(cheat_times)
  pprint([[key, len(list(group))] for key, group in grouped_times])
  return len([_ for _, saved_time in cheat_times if saved_time >= 100])