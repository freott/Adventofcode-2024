# A = (Px * By - Bx * Py) / (Ax * By - Bx * Ay)

def read(data: str):
  machines = []
  for config in data.split('\n\n'):
    a, b, p = [row.split(', ') for row in config.splitlines()]
    ax, bx = [int(str.split('X+')[1]) for str in [a[0], b[0]]]
    ay, by = [int(str.split('Y+')[1]) for str in [a[1], b[1]]]
    px = int(p[0].split('X=')[1])
    py = int(p[1].split('Y=')[1])
    machines.append((ax, ay, bx, by, px, py))
  return machines

def run(data: str) -> int:
  machines = read(data)
  tokens = 0
  for ax, ay, bx, by, px, py in machines:
    a = (px * by - bx * py) / (ax * by - bx * ay)
    if a % 1 != 0 or (px - a * ax) % bx != 0 or (py - a * ay) % by != 0: 
      continue
    b = (px - a * ax) / bx
    tokens += a * 3 + b
  return int(tokens)