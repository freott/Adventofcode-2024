def read(data: str):
  groups = [data[i:i+2] for i in range(0, len(data), 2)]
  return [list(map(int, group)) for group in groups]

def run(data: str, *args) -> int:
  groups = read(data)
  result = []
  for i, group in enumerate(groups):
    file_count, space_count = group
    for _ in range(file_count): 
      result.append(i)
    for _ in range(space_count): 
      last_i = len(groups) - 1
      if last_i == i: continue
      result.append(last_i)
      groups[last_i][0] -= 1
      if groups[last_i][0] == 0:
        del groups[last_i]
        
  return sum([value * i for i, value in enumerate(result)])