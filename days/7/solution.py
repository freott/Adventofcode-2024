from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from typing import List, NamedTuple, Tuple

class Equation(NamedTuple):
    result: int
    numbers: List[int]
    
def read(data: str) -> List[Equation]:
    return [
        Equation(int(result), list(map(int, numbers.split())))
        for row in data.splitlines() if row
        for result, numbers in [row.split(': ')]
    ]
    
def validate(curr_val: int, expected_val: int, numbers: List[int]):
    if curr_val > expected_val: return False
    if len(numbers) == 0:
        if curr_val == expected_val: return True
        return False
    number = numbers[0]
    return (
        validate(curr_val + number, expected_val, numbers[1:])
        or validate(curr_val * number, expected_val, numbers[1:])
        or (
            running_part == 2 
            and validate(
                curr_val * (10 ** len(str(number))) + number, 
                expected_val, 
                numbers[1:]
            )
        )
    )
    
def process_equation(args: Tuple[int, Equation]):
    running_part_input, eq = args
    global running_part
    running_part = running_part_input
    return eq.result if validate(eq.numbers.pop(0), eq.result, eq.numbers) else 0

def run(data: str, *args):
    equations = read(data)

    from multiprocessing import Pool
    with Pool() as pool:
        results = pool.map(process_equation, [(running_part, eq) for eq in equations])
    
    total_result = sum(results)
    return total_result
    
def part1(data: str) -> int:
    global running_part
    running_part = 1
    return run(data)

def part2(data) -> int:
    global running_part
    running_part = 2
    return run(data)