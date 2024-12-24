import networkx as nx

wires: dict[str, int]
gates: dict[str, tuple[str, str, str]]

def read(data: str):
  global wires, gates
  part1, part2 = data.split('\n\n')
  wires = {}
  for row in part1.splitlines():
    wire, value = row.split(': ')
    wires[wire] = int(value)
  gates = {}
  for row in part2.splitlines():
    rest, wire = row.split(' -> ')
    w1, operator, w2 = rest.split(' ')
    gates[wire] = (w1, w2, operator)
    
def topological_sort():
  dependencies = []
  for wire, (w1, w2, _) in gates.items():
    dependencies.append((w1, wire))
    dependencies.append((w2, wire))
  graph = nx.DiGraph(dependencies)
  return list(nx.topological_sort(graph))

OPERATORS = {
  'AND': lambda x, y: x & y,
  'XOR': lambda x, y: x ^ y,
  'OR': lambda x, y: x | y
}

def run(data: str, *args) -> int:
  read(data)
  
  for wire in topological_sort():
    if wire in wires: continue
    w1, w2, operator = gates[wire]
    wires[wire] = OPERATORS[operator](wires[w1], wires[w2])
    
  sorted_z = sorted([
    (int(wire[1:]), wires[wire]) 
    for wire 
    in wires.keys() 
    if wire[0] == 'z'
  ], reverse=True)
  
  return int(''.join(str(value) for _, value in sorted_z), 2)
    
  
