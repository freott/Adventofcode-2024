from functools import lru_cache
from itertools import permutations
from typing import Dict, List, Tuple

Map = List[Dict[str, Tuple[int, int]]]
Pad = List[List[str]]

def read(data: str): return data.splitlines()

numpad: Pad = [
  ['7', '8', '9'],
  ['4', '5', '6'],
  ['1', '2', '3'],
  [' ', '0', 'A'],
]
numpad_map: Map = {numpad[row][col]: (row, col) for row in range(len(numpad)) for col in range(len(numpad[row]))}

keypad: Pad = [
  [' ', '^', 'A'],
  ['<', 'v', '>']
]
keypad_map: Map = {keypad[row][col]: (row, col) for row in range(len(keypad)) for col in range(len(keypad[row]))}

dd = {
  '^': [-1, 0],
  '>': [0, 1],
  'v': [1, 0],
  '<': [0, -1],
}

@lru_cache(None)
def validate_seq(seq: str, pos: Tuple[int, int], use_numpad: bool):
  pad = numpad if use_numpad else keypad
  y, x = pos
  for dir in seq:
    y += dd[dir][0]
    x += dd[dir][1]
    if pad[y][x] == ' ': return False
  return True

@lru_cache(None)
def get_sequences(code: str, pointer: str, use_numpad: bool):
  map = numpad_map if use_numpad else keypad_map
  seqs = []
  for char in code:
    seq = ''
    pos = map[pointer]
    dest = map[char]
    diff_y, diff_x = tuple(a - b for a, b in zip(dest, pos))
    if diff_y > 0: seq += 'v' * diff_y
    if diff_x > 0: seq += '>' * diff_x
    if diff_x < 0: seq += '<' * abs(diff_x)
    if diff_y < 0: seq += '^' * abs(diff_y)
    unique_permutations = set(permutations(seq))
    possible_seqs = [''.join(p) for p in unique_permutations]
    max_length = max(len(s) for s in possible_seqs)
    valid_seqs = [
      ps + 'A' for ps 
      in possible_seqs 
      if len(ps) == max_length and validate_seq(ps, pos, use_numpad)
    ]
    seqs.append(valid_seqs)
    pointer = char
  return seqs

@lru_cache(None)
def operate(code: str, use_numpad: bool, depth: int):
  depth = depth - 1
  all_character_seqs = get_sequences(code, 'A', use_numpad)
  result = 0
  for character_seqs in all_character_seqs:
    shortest_op_length = float('inf')
    for seq in character_seqs:
      length = float('inf')
      
      if depth == 0:
        length = len(seq)
      else: 
        length = operate(''.join(seq), False, depth)
        
      if length < shortest_op_length:
        shortest_op_length = length
        
    result += shortest_op_length
  
  return result
  
def run(data: str, *args) -> int:
  codes = read(data)
  
  results = 0
  for code in codes:
    min = operate(code, True, 26)
    results += min * int(code[:3])
  return results
