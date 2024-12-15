from typing import List

dd = {
  '^': (-1, 0),
  '>': (0, 1),
  'v': (1, 0),
  '<': (0, -1)
}

def read(data: str):
  grid_str, moves_str = data.split('\n\n')
  grid_str = (grid_str
    .replace("#", "##")
    .replace("O", "[]")
    .replace(".", "..")
    .replace("@", "@.")
  )
  grid_rows = grid_str.splitlines()
  grid = [['' for _ in range(len(grid_rows[0]))] for _ in range(len(grid_rows))]
  robot = None
  for y, row in enumerate(grid_str.splitlines()):
    for x, cell in enumerate(row):
      grid[y][x] = cell
      if cell == '@': robot = [y, x]
  moves = [move for move in moves_str if move != '\n']
  return grid, moves, robot

def is_box_part(value: str): return value == '[' or value == ']'

def push(grid: List[List[str]], box_pos: List[int], dir: str, dry_run: bool, ignore_sibling: bool):
  box_y, box_x = box_pos
  box = grid[box_y][box_x]
  target_y, target_x = [box_y + dd[dir][0], box_x + dd[dir][1]]
  target = grid[target_y][target_x]
  sideways = box_y == target_y
  
  if sideways:
    box2_x = target_x
    
    target_x = target_x + dd[dir][1]
    target = grid[box_y][target_x]
    if target == '#': return False
    if target == '[' or target == ']':
      if not push(grid, [box_y, target_x], dir, dry_run, False):
        return False
    if not dry_run:
      grid[box_y][box2_x] = '[' if dir == '>' else ']'
      grid[box_y][target_x] = ']' if dir == '>' else '['
    return True
  else:
    box2_x = box_x + (1 if box == '[' else -1)
    box_2 = grid[box_y][box2_x]
    target2 = grid[target_y][box2_x]
    if target == '#' or target2 == '#': return False  
    
    pushing_siblings = False
    if is_box_part(target2) and is_box_part(target):
      left_side = target if box_x < box2_x else target2
      if left_side == '[':
        pushing_siblings = True
    
    if is_box_part(target):
      if not push(grid, [target_y, box_x], dir, dry_run, pushing_siblings): return False
    if not pushing_siblings and is_box_part(target2):
      if not push(grid, [target_y, box2_x], dir, dry_run, pushing_siblings): return False
      
    if not dry_run:
      grid[box_y][box_x] = '.'
      grid[box_y][box2_x] = '.'
      grid[target_y][box_x] = box
      grid[target_y][box2_x] = box_2
    return True

def run(data: str, *args) -> int:
  grid, moves, robot = read(data)
  for dir in moves:
    y, x = robot
    next_y, next_x = [y + dd[dir][0], x + dd[dir][1]]
    dest = grid[next_y][next_x]
    
    if dest == '#': continue
  
    if dest == '[' or dest == ']':
      if not push(grid, [next_y, next_x], dir, True, False):
        continue
      push(grid, [next_y, next_x], dir, False, False)

    grid[y][x] = '.'
    grid[next_y][next_x] = '@'
    robot = [next_y, next_x]
    
  result = 0
  for y, row in enumerate(grid):
    for x, cell in enumerate(row):
      if cell == '[':
        result += 100 * y + x
  return result