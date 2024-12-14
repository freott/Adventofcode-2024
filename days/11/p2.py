import math
from typing import Dict
  
def count_stones(stone: int, cache: Dict[int, int], i):
  if (stone, i) in cache: return cache[(stone, i)]
  
  count = 0
  if i == 0: return count + 1
  if stone == 0: count += count_stones(1, cache, i - 1)
  elif stone != 0 and (digits_count := math.floor(math.log10(stone)) + 1) % 2 == 0:
    divisor = 10 ** (digits_count // 2)
    count += count_stones(stone // divisor, cache, i - 1)
    count += count_stones(stone % divisor, cache, i - 1)
  else:
    count += count_stones(stone * 2024, cache, i - 1)
  
  cache[(stone, i)] = count
  return count
  

def run(data: str, *args) -> int:
  stones = list(map(int, data.split(' ')))
  cache = {}
  count = 0
  for stone in stones:
    
    count += count_stones(stone, cache, 75)
        
  return count