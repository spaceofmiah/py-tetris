from itertools import chain
import sys



# L, Q, Z, S, T, I, J
BLOCK_L = [
    [1, 0],
    [1, 0],
    [1, 1]
]

BLOCK_Q = [
    [1, 1],
    [1, 1]
]

BLOCK_Z = [
    [1, 1, 0],
    [0, 1, 1]
]

BLOCK_S = [
    [0, 1, 1],
    [1, 1, 0]
]

BLOCK_T = [
    [1, 1, 1],
    [0, 1, 0]
]

BLOCK_I = [
    [1, 1, 1, 1]
]

BLOCK_J = [
    [0, 1],
    [0, 1],
    [1, 1]
]

initial_grid = []
block_map = {
    'Q': BLOCK_Q,       
    'J': BLOCK_J,       
    'L': BLOCK_L,       
    'Z': BLOCK_Z,       
    'S': BLOCK_S,       
    'I': BLOCK_I,
    'T': BLOCK_T
}



class Tetris():
    def __init__(self, block=[[0 for _ in range(10)]]):
        self.initial_grid = block
        self.input_rows = []
        self.input_columns = []
        pass

    @property
    def height(self):
        return len(self.initial_grid)

    def put_block(self, block, position):
        base_row = len(self.initial_grid) + 1
        grid_height = len(self.initial_grid)
        grid_width = len(self.initial_grid[0])
        pad_row = 0
        pad_column = 0
        width, height, indexes = (10, 1, [])

        while True:
            has_overlap, next_width, next_height, next_indexes = self._check_overlap(
                block, self.initial_grid, base_row, position)
            if has_overlap:
                # print('found', base_row)
                break
            elif (base_row == 1):
                width, height, indexes = (
                    next_width, next_height, next_indexes)
                break
            else:
                width, height, indexes = (
                    next_width, next_height, next_indexes)
                base_row -= 1

        if (width > grid_width):
            pad_row = width - grid_width
            # TODO: IF the requirement say so for horizontally overflowing block
            pass

        if (height > grid_height):
            pad_column = height - grid_height
            padding = [[0 for _ in range(grid_width)]
                       for _ in range(pad_column)]
            self.initial_grid = padding + self.initial_grid
        for (row, column) in indexes:
            self.initial_grid[row + pad_column][column + pad_row] = 1
        
        self.remove_occupied_row()
        return self.initial_grid

    def remove_occupied_row(self):
        """Removes fully occupied row"""
        for row in range(len(self.initial_grid) - 1):
            if (0 not in self.initial_grid[row]):
                self.initial_grid.pop(row)
                if len(self.initial_grid) == 0:
                    self.initial_grid.append([0 for _ in range(10)])

    def print(self):
        from pprint import pprint
        pprint(self.initial_grid)

    def _check_overlap(self,
                       incoming_block, base_block, row_coef=1,
                       column_coef=1):
        indexes = []
        # TODO: add check coeficient cannot be less than 1
        row_coef -= 1
        column_coef -= 1

        height = len(base_block)
        width = len(base_block[0])

        row, column = (len(incoming_block), len(incoming_block[0]))
        base_row, base_column = (len(base_block) - row_coef, column_coef)

        has_overlap = False
        should_increase_height = False
        should_increase_width = False

        for i in reversed(range(row)):
            for j in range(column):
                cell = incoming_block[i][j]
                base_i = base_row - (row - i)
                base_j = base_column + j

                if (base_i < 0):
                    should_increase_height = True
                    if (cell == 1):
                        indexes.append((base_i, base_j))
                    continue

                if (base_j < 0):
                    should_increase_width = True
                    continue

                solid_cell = base_block[base_i][base_j]
                if (cell == 1 and solid_cell == 1):
                    has_overlap = True
                    break
                elif (cell == 1):
                    indexes.append((base_i, base_j))
                else:
                    continue
            if has_overlap:
                break

        if (should_increase_width):
            width = column_coef + column

        if (should_increase_height):
            height = row_coef + row
        # print(has_overlap, width, height, indexes)
        return (has_overlap, width, height, indexes)


if __name__ == "__main__":
    blocks = list(chain.from_iterable([i.split(',') for i in sys.argv[1].split('\n')]))

    tetris = Tetris()
    for block in blocks:
        block = block.replace("\n", "")
        block, position = block_map[block[0]], int(block[-1]) + 1

        tetris.put_block(block=block, position=position)
        
    print(tetris.height)
