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
  
  validate = lambda x,y: x >= 0 and x <= maxX and y >= 0 and y <= maxY
  
  for freq in freqMap.keys():
    for a, b in combinations(freqMap[freq], 2):
      xDiff = a[0] - b[0]
      yDiff = a[1] - b[1]
      aAnti = (a[0] + xDiff, a[1] + yDiff)
      bAnti = (b[0] - xDiff, b[1] - yDiff)
      if validate(aAnti[0], aAnti[1]): antinodes.add(aAnti)
      if validate(bAnti[0], bAnti[1]): antinodes.add(bAnti)
  
  return len(antinodes)