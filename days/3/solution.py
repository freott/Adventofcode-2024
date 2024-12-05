import re
    
def part1(data: str):
    def getInstructions(data: str):
        pattern = r'(mul\(\d{1,3},\d{1,3}\))'
        return re.findall(pattern, data)


    def calcInstruction(instruction: str):
        pattern = r'(mul)\((\d{1,3}),(\d{1,3})\)'
        match = re.match(pattern, instruction)
        if not match:
            raise ValueError("Invalid instruction format")
        
        operator, *values = match.groups()
        numbers = list(map(int, values))
        
        operations = {
            'mul': lambda a,b: a * b
        }
        
        if operator in operations:
            return operations[operator](*numbers)
        else:
            raise ValueError(f"Unsupported operation: {operator}")
        
    instructions = getInstructions(data)
    return sum(map(calcInstruction, instructions))


def getInstructions(data: str):
    pattern = r"(mul|do|don't)\((?:(\d{1,3},\d{1,3})?)?\)"
    return re.findall(pattern, data)

def calcInstruction(instruction: tuple[str, str]):
    operator, values = instruction
    numbers = list(map(int, filter(None, values.split(',')))) if values.strip() else []
    
    operations = {
        'mul': lambda a,b: a * b,
        'do': lambda: True,
        'don\'t': lambda: False
    }
    
    if operator in operations:
        return operations[operator](*numbers)
    else:
        raise ValueError(f"Unsupported operation: {operator}")


def part2(data) -> int:
    instructions = getInstructions(data)
    results = list(map(calcInstruction, instructions))
    total = 0
    do = True
    for result in results:
        if isinstance(result, bool):
            do = result
        elif do is True:
            total += result
        
    return total