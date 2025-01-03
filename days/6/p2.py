import bisect
import copy
from multiprocessing import Pool
from typing import Dict, List, Literal, NamedTuple, Set, Tuple, TypedDict

CordMap = Dict[int, List[int]]
class Info(NamedTuple):
    xMap: CordMap
    xMax: int
    yMap: CordMap
    yMax: int
class Pos(TypedDict):
    x: int
    y: int
    direction: Literal['U', 'R', 'D', 'L']
    
def read(data: str):
    pos: Pos
    info = Info(
        xMap = {},
        xMax = len(data.split('\n')[0]) - 1,
        yMap = {},
        yMax = len(data.split('\n')) - 1,
    )
    for y, row in enumerate(data.split('\n')):
        for x, value in enumerate(row):
            if value == '#':
                info.xMap.setdefault(x, []).append(y)
                info.yMap.setdefault(y, []).append(x)
            elif value == '^':
                pos = {'x': x, 'y': y, 'direction': 'U'}
                
    return pos, info

def calcSteps(blockers: List[int], current: int, edge: int):
    backwards = edge == 0
    remainingBlockers = [b for b in blockers if (b < current if backwards else b > current)]
    nextBlocker = remainingBlockers[-1 if backwards else 0] if remainingBlockers else None
    
    finished = nextBlocker == None
    steps = (
        abs(edge - current) 
        if finished
        else abs(nextBlocker - current) - 1
    )
    
    return steps, finished

def step(info: Info, pos: Pos, steps: Set[Tuple[int, int]], distances: Set[Tuple[int, int, int, int]]):
    finished = False
    stuck_in_loop = False
    
    def takeSteps(axis: Literal['x', 'y'], backwards: bool, stepsCount: int):
        nonlocal stuck_in_loop
        position_before = (pos['x'], pos['y'])
        for _ in range(stepsCount):
            if backwards: pos[axis] -= 1 
            else: pos[axis] += 1
            steps.add((pos['x'], pos['y']))
        position_after = (pos['x'], pos['y'])
        distance = (position_before[0], position_before[1], position_after[0], position_after[1])
        
        if distance in distances: stuck_in_loop = True
        else: distances.add(distance)
        
    if (pos['direction'] == 'U'):
        yBlockers = info.xMap.get(pos['x'], [])
        stepsCount, finished = calcSteps(yBlockers, pos['y'], 0)
        takeSteps('y', True, stepsCount)
        pos['direction'] = 'R'
    elif (pos['direction'] == 'R'):
        xBlockers = info.yMap.get(pos['y'], [])
        stepsCount, finished = calcSteps(xBlockers, pos['x'], info.xMax)
        takeSteps('x', False, stepsCount)
        pos['direction'] = 'D'
    elif (pos['direction'] == 'D'):
        yBlockers = info.xMap.get(pos['x'], [])
        stepsCount, finished = calcSteps(yBlockers, pos['y'], info.yMax)
        takeSteps('y', False, stepsCount)
        pos['direction'] = 'L'
    elif (pos['direction'] == 'L'):
        xBlockers = info.yMap.get(pos['y'], [])
        stepsCount, finished = calcSteps(xBlockers, pos['x'], 0)
        takeSteps('x', True, stepsCount)
        pos['direction'] = 'U'
    if finished:
        return steps
    elif stuck_in_loop:
        return -1
    else:
        return step(info, pos, steps, distances)

def process_step(args: Tuple[int, int, Info, Pos]):
    x, y, info, pos = args
    addedObstacle = False
    
    yMap = copy.deepcopy(info.yMap)
    if x not in yMap.get(y, []):
        addedObstacle = True
        yMap.setdefault(y, [])
        bisect.insort(yMap[y], x)
    
    xMap = copy.deepcopy(info.xMap)
    if y not in xMap.get(x, []):
        addedObstacle = True
        xMap.setdefault(x, [])
        bisect.insort(xMap[x], y)
    
    if not addedObstacle:
        return 0  # No obstacle added, not a looped variant
    
    new_info = info._replace(xMap=xMap, yMap=yMap)
    looped = step(new_info, pos.copy(), set(), set()) == -1
    return 1 if looped else 0

def run(data: str, *args):
  pos, info = read(data)
  
  steps = set()
  step(info, pos.copy(), steps, set())

  loopedVariantCount = 0
  with Pool() as pool:
      args_list = [(x, y, info, pos) for x, y in steps]
      results = pool.map(process_step, args_list)
      loopedVariantCount = sum(results)
          
  return loopedVariantCount