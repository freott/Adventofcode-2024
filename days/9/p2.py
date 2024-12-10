import copy


def read(data: str):
  groups = [data[i:i+2] for i in range(0, len(data), 2)]
  return [{ 
           'files': [[i for _ in range(int(group[0]))]], 
            'space_count': int(group[1]) if len(group) > 1 else 0
          } for i, group in enumerate(groups)]

def run(data: str) -> int:
  groups = read(data)
  for i, _ in reversed(list(enumerate(copy.deepcopy(groups)))):
    group = groups[i]
    original_files = group['files'][0]
    group_with_space_i = next((
      grp_i for grp_i, grp 
      in enumerate(groups) 
      if i > grp_i and grp['space_count'] >= len(original_files)), 
      None
    )
    if group_with_space_i == None: continue
    
    groups[group_with_space_i]['space_count'] -= len(original_files)
    group['space_count'] += len(original_files)
    groups[group_with_space_i]['files'].append(original_files)
    group['files'][0] = ['.'] * len(group['files'][0])
    
  result = []
  for group in groups:
    dotsCount = len([slot for group in group['files'] for slot in group if slot == '.'])
    result.extend(slot for group in group['files'] for slot in group)
    if (dotsCount != group['space_count']):
      result.extend(['.' for _ in range(group['space_count'] - dotsCount)])
        
  return sum([value * i if value != '.' else 0 for i, value in enumerate(result)])