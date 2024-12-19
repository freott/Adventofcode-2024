from typing import Set

def read(data: str):
  patterns, designs = data.split('\n\n')
  patterns = set(patterns.split(', '))
  longest_pattern = max(len(s) for s in patterns)
  designs = designs.splitlines()
  return designs, patterns, longest_pattern

def iterate(design: str, patterns: Set[str], longest_pattern: int, solvable_designs: Set[str], unsolvable_designs: Set[str]):
  if len(design) == 0 or design in solvable_designs: return 1
  if design in unsolvable_designs: return 0
  initial_design = design
  test = ''
  while len(design) > 0 and len(test) <= longest_pattern:
    test += design[:1]
    design = design[1:]

    if test in patterns and iterate(design, patterns, longest_pattern, solvable_designs, unsolvable_designs) == 1:
      solvable_designs.add(design)
      return 1
  unsolvable_designs.add(initial_design)
  return 0
    

def run(data: str, *args) -> int:
  designs, patterns, longest_pattern = read(data)
  solvable_designs = set()
  unsolvable_designs = set()
  return sum([iterate(design, patterns, longest_pattern, solvable_designs, unsolvable_designs) for design in designs])