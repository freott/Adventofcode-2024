from itertools import combinations, permutations, product
import math
from pprint import pprint
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
def validate_seq(seq: List[str], pos: Tuple[int, int], pad: Pad):
  y, x = pos
  for dir in seq:
    y += dd[dir][0]
    x += dd[dir][1]
    if pad[y][x] == ' ':
      return False
  return True

def get_sequences(code: str, pointer: str, map: Map, pad: Pad):
  seqs = []
  for char in code:
    seq = []
    pos = map[pointer]
    dest = map[char]
    diff_y, diff_x = tuple(a - b for a, b in zip(dest, pos))
    if diff_y > 0: seq.extend('v' * diff_y)
    if diff_x > 0: seq.extend('>' * diff_x)
    if diff_x < 0: seq.extend('<' * abs(diff_x))
    if diff_y < 0: seq.extend('^' * abs(diff_y))
    unique_permutations = set(permutations(seq))
    possible_seqs = [list(p) for p in unique_permutations]
    valid_seqs = [[*seq, 'A'] for seq in possible_seqs if validate_seq(seq, pos, pad)]
    seqs.append(valid_seqs)
    pointer = char
  return seqs

def operate(sequence: List['str'], operators: List[Tuple[Map, Pad]]):
  map, pad = operators[0]
  all_character_seqs = get_sequences(sequence, 'A', map, pad)
  remaining_operators = operators[1:]
  result = 0
  all_operations = ''
  for character_seqs in all_character_seqs:
    operations_count = float('inf')
    shortest_operation = ''
    for seq in character_seqs:
      count = float('inf')
      operation = ''
      if len(remaining_operators) == 0:
        count = len(seq)
        operation = ''.join(seq)
      else:
        count, operation = operate(seq, remaining_operators)
        
      if count < operations_count: 
        operations_count = count
        shortest_operation = operation
        
    all_operations += shortest_operation
    result += operations_count
  
  return result, all_operations
  
def run(data: str, *args) -> int:
  codes = read(data)
  
  operators = [
    (numpad_map, numpad),
    (keypad_map, keypad),
    (keypad_map, keypad),
  ]
  
  results = 0
  for code in codes:
    chars = list(code)
    min, operation = operate(chars, operators)
    results += min * int(code[:3])
  return results
