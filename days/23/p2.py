from typing import Dict

map: Dict[str, set] = {}
def read(data: str):
  global map
  relations = [tuple(row.split('-')) for row in data.splitlines()]
  for lhs, rhs in relations:
    map.setdefault(lhs, set()).add(rhs)
    map.setdefault(rhs, set()).add(lhs)

def run(data: str, *args) -> int:
  read(data)
  
  groups = set()
  seen = set()
  for usr1 in map.keys():
    seen.add(usr1)
    for usr2 in map[usr1]:
      if usr2 in seen: continue
      group = set()
      for usr3 in map[usr1].intersection(map[usr2]):
        if any(usr4 not in map[usr3] for usr4 in group):
          continue
        group.add(usr3)
      group.add(usr1)
      group.add(usr2)
      groups.add(tuple(sorted(group)))
      
  return ','.join(max(groups, key=len))