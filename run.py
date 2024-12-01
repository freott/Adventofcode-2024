import importlib
import os
import sys

def run_solution(day):
    day_folder = f"days/{day}"
    solution_file = os.path.join(day_folder, "solution.py")
    input_file = os.path.join(day_folder, "input.txt")

    if not os.path.exists(solution_file):
        print(f"Solution for Day {day} not found!")
        return

    if not os.path.exists(input_file):
        print(f"Input file for Day {day} not found!")
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
    print("Part 1:", solution.part1(data))
    print("Part 2:", solution.part2(data))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_day.py <day_number>")
        sys.exit(1)

    day_number = int(sys.argv[1])
    run_solution(day_number)