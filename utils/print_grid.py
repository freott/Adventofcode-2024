def print_grid(grid, render_cell):
  print("   ", end="")
  for col in range(len(grid[0])):
    print(col, end=" " if col > 9 else "  ")
  print()
  for i, row in enumerate(grid):
    print(i, end=" " if i > 9 else "  ")
    for cell in row:
      print(render_cell(cell), end="  ")
    print()