from collections import deque
from pprint import pprint
from typing import List

def read(data: str):
  grid_rows = data.splitlines()
  grid = [['' for _ in range(len(grid_rows[0]))] for _ in range(len(grid_rows))]
  visited_grid = [[float('inf') for _ in range(len(grid_rows[0]))] for _ in range(len(grid_rows))]
  start = None
  end = None
  for y, row in enumerate(grid_rows):
    for x, cell in enumerate(row):
      grid[y][x] = cell
      if cell == 'S': start = (y, x)
      if cell == 'E': end = (y, x)
  return grid, visited_grid, start, end

dd = [[-1, 0], [0, 1], [1, 0], [0, -1]]

def get_pos (pos: List[int], dir: int):
  return (pos[0] + dd[dir][0], pos[1] + dd[dir][1])

allowed = ['.', 'E', 'S']
def get_paths(grid: List[List[int]], start_pos: List[int], start_dir: int):
    results = []
    for dir, score in [
      [start_dir % 4, 1], 
      [(start_dir - 1) % 4, 1001], 
      [(start_dir + 1) % 4, 1001]
    ]:
      pos = get_pos(start_pos, dir)
      if grid[pos[0]][pos[1]] in allowed:
        results.append([pos, score, dir])
    
    return results

def run(data: str, *args) -> int:
  grid, visited_grid, start, end = read(data)
  visited_grid2 = visited_grid.copy()
  
  queue = deque([(start, 1, 0)])
  best_score = float('inf')

  while queue:
    pos, dir, score = queue.popleft()
    if score > best_score:
      continue
    if pos == end:
      best_score = min(best_score, score)
      continue
    if score >= visited_grid[pos[0]][pos[1]]:
      continue
    
    visited_grid[pos[0]][pos[1]] = score
    
    for p, s, d in get_paths(grid, pos, dir):
      queue.append((p, d, score + s))
      
  print(best_score)
      
  queue2 = deque([(end, 2, best_score, { end })])
  print(end)
  trails = set()
  while queue2:
    pos, dir, score, trail = queue2.popleft()
    if score < 0:
      continue
    if pos == start:
      trails = trails | trail
      print('Found one')
      continue
    # if score < visited_grid2[pos[0]][pos[1]]:
    #   continue
    
    # visited_grid[pos[0]][pos[1]] = score
    
    for p, s, d in get_paths(grid, pos, dir):
      new_trail = trail.copy()
      new_score = score - s
      new_trail.add(pos)
      queue2.append((p, d, new_score, new_trail))
  print(trails)
  return len(trails)