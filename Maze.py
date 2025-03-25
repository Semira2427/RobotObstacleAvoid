import random

def make_maze(width, height):
    grid = [['#'] * width for _ in range(height)]

    def carve_path(x, y):
        grid[y][x] = ' '
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width - 1 and 0 < ny < height - 1 and grid[ny][nx] == '#':
                grid[ny - dy // 2][nx - dx // 2] = ' '
                carve_path(nx, ny)

    start_x, start_y = 1, 1
    carve_path(start_x, start_y)
    grid[start_y][start_x] = 'S'
   
    for i in range(height):
      if grid[i][width-2] == ' ':
        grid[i][width-1] = 'E'
        break
   
    return grid

def print_maze(maze):
    for row in maze:
        print(''.join(row))

width, height = 21, 15
maze = make_maze(width, height)
print_maze(maze)
