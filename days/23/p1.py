from typing import Dict

def read(data: str):
  return [tuple(row.split('-')) for row in data.splitlines()]

def run(data: str, *args) -> int:
  relations = read(data)
  map: Dict[str, set] = {}
  for lhs, rhs in relations:
    map.setdefault(lhs, set()).add(rhs)
    map.setdefault(rhs, set()).add(lhs)
  
  triples = set()
  for usr1 in map.keys():
    if usr1[0] != 't': continue
    for usr2 in map[usr1]:
      for usr3 in map[usr1].intersection(map[usr2]):
        triple = (usr1, usr2, usr3)
        triples.add(tuple(sorted(triple)))
        
  return len(triples)