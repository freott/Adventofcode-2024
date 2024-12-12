import math

def run(data: str) -> int:
  stones = list(map(int, data.split(' ')))
  for _ in range(25):
    next_stones = []
    for stone in stones:      
      if stone == 0: next_stones.append(1)
      elif stone != 0 and (digits_count := math.floor(math.log10(stone)) + 1) % 2 == 0:
        divisor = 10 ** (digits_count // 2)
        next_stones.append(stone // divisor)
        next_stones.append(stone % divisor)
      else:
        next_stones.append(stone * 2024)
    stones = next_stones
        
  return len(stones)