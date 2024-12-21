from itertools import product
from typing import Dict, List, Optional, Tuple


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

def resolve_paths(
  grid: List[List[int]], 
  start: Tuple[int, int], 
  end: Tuple[int, int],
  resolved_paths: Dict[Tuple[int, int], int] = {}
):
  batch = [[start]]
  
  steps = -1
  while batch:
    steps += 1
    next_batch = []
    for path in batch:
      pos = path[-1]
      if pos in resolved_paths: 
        for i, p in enumerate(path): resolved_paths[p] = resolved_paths[pos] + steps - i
        continue
      if pos == end: 
        for i, p in enumerate(path): resolved_paths[p] = steps - i
        continue
      
      positions = get_next_positions(pos[0], pos[1], grid)
      next_batch.extend([[*path, p] for p in positions if p not in path])
    batch = next_batch
  return resolved_paths

def get_cheat_destinations(y: int, x: int):
  destinations = set()
  for py, px in product(range(21), range(21)):
    seconds = py + px
    if seconds > 20: continue
    destinations.add((y + py, x + px, seconds))
    destinations.add((y - py, x - px, seconds))
    destinations.add((y + py, x - px, seconds))
    destinations.add((y - py, x + px, seconds))
  return destinations
  

def resolve_cheats(
  grid: List[List[int]], 
  start: Tuple[int, int], 
  resolved_paths: Dict[Tuple[int, int], int],
  is_test: bool,
  cheats: Dict[Tuple[int, int], Dict[Tuple[int, int], int]] = {},
):
  batch = [start]
  steps = -1
  while batch:
    steps += 1
    next_batch = []
    for pos in batch:
      if pos in cheats: continue
      cheats[pos] = {}
      cheat_destinations = get_cheat_destinations(pos[0], pos[1])
      for cy, cx, sec in cheat_destinations:
        if (cy, cx) not in resolved_paths: continue
        cheat_time = steps + sec + resolved_paths[(cy, cx)]
        if cheat_time > resolved_paths[start] - (50 if is_test else 100): continue
        cheats[pos][(cy, cx)] = cheat_time
      
      positions = get_next_positions(pos[0], pos[1], grid)
      next_batch.extend(positions)
    batch = next_batch
  return cheats

def run(data: str, is_test, *args) -> int:
  grid, start, end = read(data)
  
  resolved_paths = resolve_paths(grid, start, end)
  cheats = resolve_cheats(grid, start, resolved_paths, is_test)
  original_time = resolved_paths[start]
  time_saved_counts = {}
  for cheat in cheats.values():
    for c_time in cheat.values():
      time_saved = original_time - c_time
      time_saved_counts.setdefault(time_saved, 0)
      time_saved_counts[time_saved] += 1
  return sum(time_saved_counts.values())