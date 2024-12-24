import networkx as nx
from graphviz import Digraph

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
  for w in topological_sort():
    if w in wires: continue
    w1, w2, operator = gates[w]
    wires[w] = OPERATORS[operator](wires[w1], wires[w2])
  
  swaps = [
    ('z16', 'fkb'), 
    ('z37','rrn'),
    ('rqf', 'nnr'),
    ('z31', 'rdn')
  ]
  # SWAPS
  for o1, o2 in swaps:
    gate1 = gates[o1]
    gate2 = gates[o2]
    gates[o1] = gate2
    gates[o2] = gate1
  
  dot = Digraph("Graph", format="png")
  dot.attr(nodesep="1.0")
  dot.attr(ranksep="1.5") 

  for w, (w1, w2, operator) in gates.items():
    dot.node(w1, w1)
    dot.node(w2, w2)
    dot.node(w, w)
    op_node = f"{w1}_{w2}_{operator}"
    dot.node(op_node, operator, shape="diamond")

    dot.edge(w1, op_node)
    dot.edge(w2, op_node)
    dot.edge(op_node, w)

  # dot.render("connections", view=True)

  return ','.join(sorted([wire for t in swaps for wire in t]))
    
  
