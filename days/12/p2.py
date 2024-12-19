from collections import deque
from typing import List, Tuple

def read(data: str):
  rows = data.splitlines()
  grid = [[] for _ in rows]
  for y, row in enumerate(rows):
    for cell in row:
      grid[y].append(cell)
      
  return grid

def in_grid(value: str, y: int, x: int, grid: List[List[int]]):
  return 0 <= y < len(grid) and 0 <= x < len(grid[0]) and value == grid[y][x]

def count_corners(region: List[Tuple[int, int]], grid: List[List[str]]):
  seen = set()
  corner_count = 0
  value = grid[region[0][0]][region[0][1]]
  for y, x in region:
    corners = [
      [y - 0.5, x - 0.5], 
      [y - 0.5, x + 0.5], 
      [y + 0.5, x + 0.5], 
      [y + 0.5, x - 0.5]
    ]
    for cy, cx in corners:
      if (cy, cx) in seen: continue
      seen.add((cy, cx))
      matches = [(int(my), int(mx)) in region and in_grid(value, int(my), int(mx), grid) for my, mx in [
        [cy - 0.5, cx - 0.5], 
        [cy - 0.5, cx + 0.5], 
        [cy + 0.5, cx + 0.5], 
        [cy + 0.5, cx - 0.5]
      ]]
      match_count = sum(matches)
      if match_count == 1: corner_count += 1
      elif match_count == 2 and (
        matches == [True, False, True, False] 
        or matches == [False, True, False, True]
      ): corner_count += 2
      elif match_count == 3: corner_count += 1
  return corner_count

dd = [[-1, 0], [0, 1], [1, 0], [0, -1]]
def get_regions(grid: List[List[str]]):
  seen = set()
  regions = []
  for y, row in enumerate(grid):
    for x, cell in enumerate(row):
      start = (y,x)
      if start in seen: continue
      seen.add(start) 
      region = [start]
      queue = deque([start])
      while queue:
        node = queue.popleft()
        for dir in range(4):
          neighbor = (node[0] + dd[dir][0], node[1] + dd[dir][1])
          if neighbor in seen: continue
          if not in_grid(cell, neighbor[0], neighbor[1], grid): continue
          seen.add(neighbor)
          region.append(neighbor)
          queue.append(neighbor)
      regions.append(region)
  return regions

def run(data: str, *args) -> int:
  grid = read(data)
  regions = get_regions(grid)
  return sum([count_corners(region, grid) * len(region) for region in regions])