from typing import List

dd = {
  '^': (-1, 0),
  '>': (0, 1),
  'v': (1, 0),
  '<': (0, -1)
}

def read(data: str):
  grid_str, moves_str = data.split('\n\n')
  grid_rows = grid_str.splitlines()
  grid = [['' for _ in range(len(grid_rows[0]))] for _ in range(len(grid_rows))]
  robot = None
  for y, row in enumerate(grid_str.splitlines()):
    for x, cell in enumerate(row):
      grid[y][x] = cell
      if cell == '@': robot = [y, x]
  moves = [move for move in moves_str if move != '\n']
  return grid, moves, robot

def try_push(grid: List[List[str]], box: List[int], dir: str):
  y, x = box
  next_y, next_x = [y + dd[dir][0], x + dd[dir][1]]
  
  dest = grid[next_y][next_x]
  if (dest == '#'):
    return False
    
  if (dest == 'O'):
    if not try_push(grid, [next_y, next_x], dir):
      return False
      
  grid[next_y][next_x] = 'O'
  return True

def run(data: str, *args) -> int:
  grid, moves, robot = read(data)
  for dir in moves:
    y, x = robot
    next_y, next_x = [y + dd[dir][0], x + dd[dir][1]]
    dest = grid[next_y][next_x]
    
    if dest == '#': continue
  
    if dest == 'O':
      if not try_push(grid, (next_y, next_x), dir):
        continue
      
    grid[y][x] = '.'
    grid[next_y][next_x] = '@'
    robot = [next_y, next_x]
    
  result = 0
  for y, row in enumerate(grid):
    for x, cell in enumerate(row):
      if cell == 'O':
        result += 100 * y + x
  return result
    