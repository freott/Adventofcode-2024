from itertools import combinations, product
from typing import Dict, List, Tuple

def read(data: str):
  freqMap: Dict[str, List[Tuple[int, int]]] = {}
  rows = data.splitlines()
  maxX = len(rows[0]) - 1
  maxY = len(rows) - 1
  for y, x in product(range(maxX + 1), range(maxY + 1)):
    char = rows[y][x]
    if char != '.':
        freqMap.setdefault(char, []).append((x, y))
  return freqMap, maxX, maxY

def run(data: str) -> int:
  freqMap, maxX, maxY = read(data)  
  
  antinodes = set()
  validate = lambda x, y: x >= 0 and x <= maxX and y >= 0 and y <= maxY
  def iterate(cords: Tuple[int, int], reverse: bool, xDiff: int, yDiff: int):
    calc = lambda x, y: (x - xDiff, y - yDiff) if reverse else (x + xDiff, y + yDiff)
    while validate(cords[0], cords[1]):
      antinodes.add(cords)
      cords = calc(cords[0], cords[1])
      
  for cordList in freqMap.values():
    for a, b in combinations(cordList, 2):
      xDiff = a[0] - b[0]
      yDiff = a[1] - b[1]
        
      iterate(a, False, xDiff, yDiff)
      iterate(b, True, xDiff, yDiff)
  
  return len(antinodes)