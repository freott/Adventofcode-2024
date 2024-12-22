from collections import deque
from functools import lru_cache
from typing import List, Tuple

grid: List[List[str]] = None
start: Tuple[int, int] = None
end: Tuple[int, int] = None

def read(data: str):
  global grid, start, end
  grid_rows = data.splitlines()
  grid = [['' for _ in range(len(grid_rows[0]))] for _ in range(len(grid_rows))]
  for y, row in enumerate(grid_rows):
    for x, cell in enumerate(row):
      grid[y][x] = cell
      if cell == 'S': start = (y, x)
      if cell == 'E': end = (y, x)

dd = [[-1, 0], [0, 1], [1, 0], [0, -1]]
allowed = ['.', 'E', 'S']

@lru_cache(None)
def get_paths(pos: Tuple[int, int], dir: int):
  results = []
  for d, score in [
    [dir % 4, 1], 
    [(dir - 1) % 4, 1001], 
    [(dir + 1) % 4, 1001]
  ]:
    y, x = (pos[0] + dd[d][0], pos[1] + dd[d][1])
    if grid[y][x] in allowed:
      results.append(((y, x), d, score))
  
  return results
  
@lru_cache(None)
def resolve_path(start: Tuple[int, int], start_dir: int):
  queue = deque([(start, start_dir, 0)])
  best_score = float('inf')
  seen = {}

  while queue:
    pos, dir, score = queue.popleft()
    if score > best_score: continue
    if pos == end:
      best_score = min(best_score, score)
      continue
    if pos in seen and score >= seen[pos]:
      continue
    seen.setdefault(pos, score)
    
    for p, d, s in get_paths(pos, dir):
      queue.append((p, d, score + s))
    
  return best_score

def run(data: str, *args) -> int:
  read(data)
  best_score = resolve_path(start, 1)
  
  best_tiles = { start }
  iteratives = [(start, 1, 0, set())]
  while(iteratives):
    i = iteratives.pop(0)
    pos, dir, score, seen = i
    pos_dir = (pos, dir)
    if pos_dir in seen: continue
    seen.add(pos_dir)
    
    paths = get_paths(pos, dir)
    if not paths: continue
    
    for p, d, s in paths:
      new_score = score + s
      if resolve_path(p, d) + new_score != best_score: continue
      best_tiles.add(p)
      iteratives.append((p, d, new_score, seen.copy()))
      
  return len(best_tiles)