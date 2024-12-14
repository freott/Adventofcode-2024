def read(data: str):
  rows = data.splitlines()
  map = [[] for _ in rows]
  trailheads = []
  for y, row in enumerate(rows):
    for x, value in enumerate(row):
        val = int(value)
        map[y].append(val)
        if val == 0: trailheads.append((y, x))
  return map, trailheads

dd = [[-1, 0], [0, 1], [1, 0], [0, -1]]

def run(data: str, *args) -> int:
  map, trailheads = read(data)
  
  trailhead_scores = []
  for trailhead in trailheads:  
    ends = set()
    seen = set()
    batch = [trailhead]
    while batch:
      next_batch = []
      for pos in batch:
        if pos in seen: continue
        seen.add(pos)
        y,x = pos
        val = map[y][x]
        if val == 9:
          ends.add(pos)
          continue
        
        nextVal = val + 1
        for dir in range(4):
          next_y = y + dd[dir][0]
          next_x = x + dd[dir][1]
          if 0 <= next_y < len(map) and 0 <= next_x < len(map[0]):
            if map[next_y][next_x] == nextVal:
              next_batch.append((next_y, next_x))
        
      batch = next_batch
    trailhead_scores.append(len(ends))
  return sum(trailhead_scores)