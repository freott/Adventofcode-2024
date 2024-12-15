from itertools import combinations, product
from pprint import pprint
from typing import List, Set, Tuple

def read(data: str):
  rows = data.splitlines()
  grid = [[] for _ in rows]
  for y, row in enumerate(rows):
    for cell in row:
      grid[y].append(cell)
      
  return grid
    
dd = [[-1, 0], [0, 1], [1, 0], [0, -1]]
def count_siblings(pos: Tuple[int, int], grid: List[List[str]], handled: Set[Tuple[int, int]]):
  if pos in handled: return 0, 0
  handled.add(pos)
  count = 1
  fences = 4
  for dir in range(4):
    y, x = pos
    next_y = y + dd[dir][0]
    next_x = x + dd[dir][1]
    if 0 <= next_y < len(grid) and 0 <= next_x < len(grid[0]):
      if grid[y][x] == grid[next_y][next_x]:
        fences -= 1
        next_count, next_fences = count_siblings((next_y, next_x), grid, handled)
        count += next_count
        fences += next_fences
      
  return count, fences
    
  
    
def run(data: str, *args) -> int:
  grid = read(data)
  handled = set()
  results = []
  for y, x in product(range(len(grid)), range(len(grid[0]))):
      count, fences = count_siblings((y, x), grid, handled)
      if count == 0: continue
      
      results.append((count, fences))
      
  return sum([count * fences for count, fences in results])