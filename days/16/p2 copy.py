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

allowed = ['.', 'E']
def get_paths(grid: List[List[int]], start_pos: List[int], start_dir: int):
    results = []
    for dir, score in [
      [(start_dir - 1) % 4, 1001], 
      [(start_dir + 1) % 4, 1001],
      [start_dir % 4, 1],
    ]:
      pos = get_pos(start_pos, dir)
      if grid[pos[0]][pos[1]] in allowed:
        results.append([pos, score, dir])
    
    return results

def run(data: str, *args) -> int:
  grid, visited_grid, start, end = read(data)
  
  stack = [(start, 1, 0, { start: 0 })]
  best_score = float('inf')
  best_score_trails = set()

  while stack:
    pos, dir, score, trail = stack.pop()
    if score > best_score:
      continue
    if pos == end:
      for p, s in trail.items():
        visited_grid[p[0]][p[1]] = min(visited_grid[p[0]][p[1]], s)
      if best_score >= score:
        trail_keys = set(trail.keys())
        if best_score > score:
          best_score = score
          best_score_trails = trail_keys
        else:
          best_score_trails = best_score_trails | trail_keys
      continue
    
    visited_grid[pos[0]][pos[1]] = score
    
    for p, s, d in get_paths(grid, pos, dir):
      new_trail = trail.copy()
      if p in trail: continue
      new_score = score + s
      new_trail[p] = new_score
      stack.append((p, d, new_score, new_trail))
  
  return len(best_score_trails)