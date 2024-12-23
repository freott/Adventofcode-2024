import math

def read(data: str):
  return list(map(int, data.splitlines()))

def mix(number: int, value: int): return number ^ value
def prune(number: int): return number % 16777216

def run(data: str, *args) -> int:
  numbers = read(data)
  
  result = []
  for n in numbers:
    for _ in range(2000):
      n = mix(n, n * 64)
      n = prune(n)
      
      n = mix(n, math.floor(n / 32))
      n = prune(n)
      
      n = mix(n, n * 2048)
      n = prune(n)
    result.append(n)
    
  return sum(result)