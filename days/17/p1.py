import math

def read(data: str):
  registers, program = data.split('\n\n')
  a,b,c = [int(row.split(': ')[1]) for row in registers.splitlines()]
  program = list(map(int, program.split(': ')[1].split(',')))
  return a,b,c,program

def run(data: str, *args) -> int:
  a,b,c,program = read(data)
  
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
      output.append(to_combo(operand) % 8)
    elif opcode == 6:
      b = adv(operand)
    elif opcode == 7:
      c = adv(operand)
    pointer += 2
        
  return ','.join(list(map(str, output)))