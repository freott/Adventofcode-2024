import importlib
import os
import sys

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

    # Dynamically import the solution module
    module_name = f"days.{day}.solution"
    try:
        solution = importlib.import_module(module_name)
    except ImportError:
        print(f"Could not import solution for Day {day}.")
        return

    with open(input_file) as f:
        data = f.read().strip()

    print(f"Running Day {day}...")
    if part is None or part == 1:
        print("Part 1:", solution.part1(data))
    if part is None or part == 2:
        print("Part 2:", solution.part2(data))


if __name__ == "__main__":
    if len(sys.argv) not in [2, 3, 4]:
        print("Usage: python run_day.py <day_number> [test] [part]")
        sys.exit(1)

    day = sys.argv[1]
    test = False
    part = None

    if len(sys.argv) >= 3:
        if sys.argv[2].lower() == "test":
            test = True
            if len(sys.argv) == 4:
                part = int(sys.argv[3])
        else:
            part = int(sys.argv[2])

    run_solution(day, test, part)