import math
from typing import List

def read(data: str):
  registers, program = data.split('\n\n')
  a,b,c = [int(row.split(': ')[1]) for row in registers.splitlines()]
  program = list(map(int, program.split(': ')[1].split(',')))
  return a,b,c,program

def run_program(a: int, b: int, c: int, program: List[int]):
  def to_combo(operand):
    if operand < 4: return operand
    if operand == 4: return a
    if operand == 5: return b
    if operand == 6: return c
    
  def adv(operand):
    return math.trunc(a / (2 ** to_combo(operand)))
  
  output = []
  pointer = 0
  while 0 <= pointer < len(program):
    opcode, operand = program[pointer], program[pointer + 1]
    if opcode == 0:
      a = adv(operand)
    elif opcode == 1:
      b = b ^ operand
    elif opcode == 2:
      b = to_combo(operand) % 8
    elif opcode == 3:
      if a != 0:
        pointer = operand
        continue
    elif opcode == 4:
      b = b ^ c
    elif opcode == 5:
      val = to_combo(operand) % 8
      if program[len(output)] != val: return False
      output.append(val)
    elif opcode == 6:
      b = adv(operand)
    elif opcode == 7:
      c = adv(operand)
    pointer += 2
    
  if program != output: return False
  
  return True

def run(data: str, *args) -> int:
  a,b,c,program = read(data)
  
  a = 117440
  run_program(a, b, c, program)
  return a
  