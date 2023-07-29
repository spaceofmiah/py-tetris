from pprint import pprint
from enum import Enum
import typing
import queue


class Piece:
    """Represents a piece in the game.

    Attributes:
        space (matrix): The unit spaces that 
        makes up a piece. 
        
        A piece element with a value of  1 indicates 
        that the unit space is occupied.
        
        A piece element with a value of 0 indicates that
        the unit space is not occupied.

        sample
            a piece representing Q is a matrix
                [
                    [1, 1],
                    [1, 1]
                ]
            
            a piece representing i is a vector
                [
                    [1, 1, 1, 1]
                ]

            a piece representing L is a vector
                [
                    [1],
                    [1],
                    [1],
                    [1, 1,]
                ]

    """

    def __init__(self, space:list) -> None:
        self._space = space
    
    @property
    def space(self) -> list:
        """Get the unit spaces that make up the piece."""
        return self._space
    
    def __str__(self) -> str:
        return f'Piece: {self._space}'
    
    def __repr__(self) -> str:
        return f'Piece: {self._space}'


class PositionCheckCause(Enum):
    """Represents the cause of a position check result."""
    ROW_OUT_OF_BOUNDS   = 'row_out_of_range'
    CHECK               = 'position_check'


class PlayGround:
    """Represents the playground for the game.

    Attributes:
        width (int): The width of the playground.
        This represents the number of units that can
        occupy a row in a grid. defaults to 10.
    """

    def __init__(self, width=10) -> None:
        self._width = width
        self._row  = ['-'] * width
        self._grid = [self._row]
    
    def initialize_row(self):
        """Reinitialize the current play row."""
        self._row = ['-'] * self._width
    
    def occupy_between(self, start:int, end:int) -> None:
        """Occupy the playground between the given indices.

        Args:
            start (int): The starting index.
            end (int): The ending index.
        """
        for index in range(start, end):
            if self.is_unit_empty(index):
                self._row[index] = 'o'
            else:
                print(f'Unit {index} is occupied. Cannot occupy')
                self._grid.append(self._row)
                self.initialize_row()
                self._row[index] = 'o'
    
    def place_piece(self, piece:Piece, at:int) -> None:
        """Place the given piece on the playground.

        Args:
            piece (Piece): The piece to place.
            xy_position (int): The xy position of the piece.
        """
        row = 0

        # GET POTENTIAL STARTING ROW
        # finding row for the column( at ) where piece placement can commence 
        # in the playground
        while row < len(self._grid):
            is_space_empty, reason = self.position_emptiness_check_and_cause(row=row, col=at)
            if not is_space_empty and reason == PositionCheckCause.ROW_OUT_OF_BOUNDS:
                self.initialize_row()
                self._grid.append(self._row)
                row += 1
            else:
                # CHECK PIECE HEIGHT AND MAKE SURE SPACE ABOVE START ROW CAN HOLD PIECE DATA
                total_piece_height = len(piece.space) - 1
                if total_piece_height > 1:
                    height_counter = 1
                    while height_counter <= total_piece_height:
                        row_above_current_row = row + height_counter
                        is_space_empty, reason = self.position_emptiness_check_and_cause(row=row_above_current_row, col=at)
                        if not is_space_empty and reason == PositionCheckCause.CHECK:
                            row += 1
                        height_counter += 1
                break

        # bottom pieces first 
        reversed_pieces = reversed(piece.space)

        # Everything is just a vector at the end of the day
        for piece_vector in reversed_pieces:
            next_col = 0

            # if the vector element cannot all contain single row,
            # add new row and increment the row to commence placement
            for item in piece_vector:
                if item == 1:
                    if not self.is_unit_empty(unit_index=at + next_col, play_row=self._grid[row]):
                        if row == len(self._grid) - 1:
                            self.initialize_row()
                            self._grid.append(self._row)
                        row += 1
                next_col += 1
            
            # having found the row a piece could commence, if the piece
            # containment would take more than a row, then the piece needs
            # row higher up needs to be empty as well. Imagine 
            # l0   -> this would have a good placement 
            # l1   -> this would have a good placement
            # i4   -> this would have a good start placement but the row higher up would've been occupied by l1
            '''
                    o   o   o   o            
                o   o   o   o   # tyring to place 14 here would be fine but right above it, there already is a placement
            '''
            
            next_col = 0
            current_play_row = self._grid[row]

            for item in piece_vector:
                if item == 1: 
                    current_play_row[at + next_col] = 'o'
                next_col += 1


    def is_unit_empty(self, unit_index:int, play_row:[]=None) -> bool:
        """Check if the given unit is empty.

        Args:
            unit_index (int): The index of the unit position in a grid.

        Returns:
            bool: True if the unit is empty.
        """
        if unit_index >= self._width:
            return False
        else:
            if play_row: return play_row[unit_index] == '-'
            return self._row[unit_index] == '-'
    
    def position_emptiness_check_and_cause(self, row:int, col:int) -> typing.Tuple[bool, str]:
        """Check if the given grid position is empty.

        Args:
            x (int): The x position of the grid.
            y (int): The y position of the grid.

        Returns:
            bool: True if the grid position is empty.
        """
        if row >= len(self._grid):
            print(f'Grid position {row} is out of bounds. Cannot check if empty')
            return False, PositionCheckCause.ROW_OUT_OF_BOUNDS
        return self._grid[row][col] == '-', PositionCheckCause.CHECK

    def output_current_play_ground(self):
        """Output the current play ground."""
        pprint(list(reversed(self._grid)))


if __name__ == '__main__':
    play_ground = PlayGround()
    l_piece = Piece([[1, 1, 1, 1]])
    i_piece = Piece(
        [
            [1],
            [1],
            [1, 1]
        ]
    )
    play_ground.place_piece(l_piece, 0)
    play_ground.place_piece(l_piece, 1)
    play_ground.place_piece(l_piece, 5)  
    play_ground.place_piece(l_piece, 5)
    play_ground.place_piece(i_piece, 4)
    play_ground.place_piece(l_piece, 0)
    play_ground.place_piece(l_piece, 0)
    play_ground.place_piece(l_piece, 0)
    play_ground.place_piece(l_piece, 6)
    play_ground.output_current_play_ground()

    
    

