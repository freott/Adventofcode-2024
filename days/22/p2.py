import math
from pprint import pprint

def read(data: str):
  return list(map(int, data.splitlines()))

def mix(number: int, value: int): return number ^ value
def prune(number: int): return number % 16777216
def get_price(number: int): return number % 10

def run(data: str, *args) -> int:
  numbers = read(data)
  
  all_results = {}
  for n in numbers:
    result = {}
    prev_price = get_price(n)
    sequence = []
    for _ in range(2000):
      n = mix(n, n * 64)
      n = prune(n)
      
      n = mix(n, math.floor(n / 32))
      n = prune(n)
      
      n = mix(n, n * 2048)
      n = prune(n)
      
      price = get_price(n)
      diff = price - prev_price
      prev_price = price
      sequence.append(diff)
      if len(sequence) > 4:
        sequence.pop(0)
        sequence_tuple = tuple(sequence)
        result.setdefault(sequence_tuple, price)    
  
    for seq, price in result.items():
      all_results.setdefault(seq, 0)
      all_results[seq] += price
      
  return max(all_results.values())