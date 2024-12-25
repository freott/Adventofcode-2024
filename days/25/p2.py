from itertools import product

keys = []
locks = []

def read(data: str):
  schemas = data.split('\n\n')
  for schema in schemas:
    columns = []
    for row in schema.splitlines()[1:-1]:
      for x, value in enumerate(row):
        if x >= len(columns):
          columns.append(0)
        if value == '#': columns[x] += 1
    if schema[0] == '#': locks.append(columns)
    else: keys.append(columns)


def run(data: str, *args) -> int:
  read(data)
  results = 0
  for key, lock in product(keys, locks):
    failed = False
    for k, l in zip(key, lock):
      if failed: break
      if k + l > 5: failed = True
    if not failed: results += 1
  return results