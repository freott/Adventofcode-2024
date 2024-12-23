from typing import Dict, Set

def read(data: str):
  patterns, designs = data.split('\n\n')
  patterns = set(patterns.split(', '))
  longest_pattern = max(len(s) for s in patterns)
  designs = designs.splitlines()
  return designs, patterns, longest_pattern

def iterate(design: str, patterns: Set[str], longest_pattern: int, solvable_designs: Dict[str, int], unsolvable_designs: Set[str]):
  if len(design) == 0: return 1
  if design in solvable_designs: return solvable_designs[design]
  if design in unsolvable_designs: return 0
  initial_design = design
  test = ''
  solvable_count = 0
  while len(design) > 0 and len(test) <= longest_pattern:
    test += design[:1]
    design = design[1:]

    if test in patterns:
      count = iterate(design, patterns, longest_pattern, solvable_designs, unsolvable_designs)
      if count > 0:  
        solvable_designs.setdefault(design, count)
        solvable_count += count
      else:
        unsolvable_designs.add(initial_design)
        
  return solvable_count
    

def run(data: str, *args) -> int:
  designs, patterns, longest_pattern = read(data)
  solvable_designs = {}
  unsolvable_designs = set()
  return sum([iterate(design, patterns, longest_pattern, solvable_designs, unsolvable_designs) for design in designs])