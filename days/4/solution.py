from typing import Dict, List, Literal, Tuple

Directions = Literal['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']
ALL_DIRECTIONS = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']
def get_cord(cord: Tuple[int, int], direction: str): 
    direction_map = {
        "N": (cord[0], cord[1] - 1),
        "S": (cord[0], cord[1] + 1),
        "E": (cord[0] + 1, cord[1]),
        "W": (cord[0] - 1, cord[1]),
        "NE": (cord[0] + 1, cord[1] - 1),
        "NW": (cord[0] - 1, cord[1] - 1),
        "SE": (cord[0] + 1, cord[1] + 1),
        "SW": (cord[0] - 1, cord[1] + 1),
    }
    return direction_map[direction]

def get_cord_map(data: str):
    cords = {}
    rows = data.split('\n')
    for rowI, row in enumerate(rows):
        for colI, value in enumerate(row):
            cords[colI, rowI] = value
    return cords

def iterate(
        cord: Tuple[int, int], 
        chars: List[str],
        direction: Directions,
        cord_map: Dict[Tuple[int, int], str]
    ):
        if not chars: return True
        nextChar = chars.pop(0)
        if cord not in cord_map: return False
        if cord_map[cord] != nextChar: return False
        else:   
            return iterate(get_cord(cord, direction), chars, direction, cord_map)

def part1(data: str) -> int:
    cord_map = get_cord_map(data)
    chars = ['X','M','A','S']
    result = 0
    for cord in cord_map:
        for direction in ALL_DIRECTIONS:
            if iterate(cord, chars[:], direction, cord_map):
                result += 1
            
    return result


def part2(data):
    cord_map = get_cord_map(data)
    chars = ['M','A','S']
    result = 0
    for cord in cord_map:
        if cord_map[cord] is not 'A': continue
        if ((
                iterate(get_cord(cord, 'NW'), chars[:], 'SE', cord_map)
                or iterate(get_cord(cord, 'SE'), chars[:], 'NW', cord_map)
            ) and (
                iterate(get_cord(cord, 'NE'), chars[:], 'SW', cord_map)
                or iterate(get_cord(cord, 'SW'), chars[:], 'NE', cord_map)
            )
        ): 
            result += 1
    return result