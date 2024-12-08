import importlib
import os
import sys
import time
from colorama import Fore, Style

BRIGHT_GREEN = "\033[32m"
RESET = "\033[0m"

def get_input_file(day: str, test: bool = False) -> str:
    return (
        os.path.join(day, "test_input.txt")
        if test
        else os.path.join(day, "input.txt")
    )

def run_solution(day, test: bool = False, part: int = None):
    day_folder = f"days/{day}"
    solution_file = os.path.join(day_folder, "solution.py")
    input_file = get_input_file(day_folder, test)

    if not os.path.exists(solution_file):
        print(f"Solution for Day {day} not found!")
        return

    if not os.path.exists(input_file):
        print(f"Input file {input_file} not found!")
        return
    
    # Dynamically add the day folder to sys.path
    sys.path.insert(0, os.path.abspath(day_folder))

    # Dynamically import the solution module
    module_name = f"days.{day}.solution"
    try:
        solution = importlib.import_module(module_name)
    except ImportError as e:
        print(f"Could not import solution for Day {day}: {e}")
        return

    with open(input_file) as f:
        data = f.read().strip()
        
    print(f"Running Day {day}...")
    def run(partNo: int):
        start = time.time()
        if partNo == 1: 
            print("Part 1:", f"{BRIGHT_GREEN}{solution.part1(data)}{RESET}", end=' ')
        elif partNo == 2: 
            print("Part 2:", f"{BRIGHT_GREEN}{solution.part2(data)}{RESET}", end=' ')
        elapsed = time.time() - start
        print(Fore.YELLOW + f"{elapsed:.6f} seconds" + Style.RESET_ALL)
        
    [run(partNo) for partNo in [1,2] if part is None or part == partNo]


if __name__ == "__main__":
    if len(sys.argv) not in [2, 3, 4]:
        print("Usage: python run_day.py <day_number> [test] [part]")
        sys.exit(1)

    day = sys.argv[1]
    test = False
    part = None

    arg2 = sys.argv[2] if len(sys.argv) > 2 else None
    arg3 = sys.argv[3] if len(sys.argv) > 3 else None
    
    for i in [2, 3]:
        arg = sys.argv[i] if len(sys.argv) > i else None
        if (arg == None): continue
        if (arg.lower() == "test"):
            test = True
        elif (arg.isdigit()):
            part = int(arg)

    run_solution(day, test, part)