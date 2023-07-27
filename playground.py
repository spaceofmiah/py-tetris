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
        self._grid = []
        self._width = width
        self._current_play_row = 0
        self._row  = ['-'] * width
    
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
        # bottom pieces first 
        reversed_pieces = reversed(piece.space) 
        # total y space occupied by the piece needs to checked for 
        # availability in the playground before placing any piece
        # total_piece_height = len(piece.space)

        # if total_piece_height > len(self._grid):
        #     # the total piece height is greater than the playground
        #     # height. This means the piece would increase the playground
        #     # by including more rows.
        #     pass

        row = 0

        # finding row for the column( at ) where piece placement can commence 
        # in the playground
        while row <= self._current_play_row:
            is_space_empty, reason = self.position_emptiness_check_and_cause(row=row, col=at)
            if is_space_empty is True:
                break
            else:
                if reason == PositionCheckCause.ROW_OUT_OF_BOUNDS:
                    self._grid.append(self._row) # add current row
                    self.initialize_row() # initialize new row
                    self._grid.append(self._row) # add new row
            row += 1
        
        
        # having found the row where piece placement is to commence
        # retrieve the vector place each scalar appropriately

        # Everything is just a vector at the end of the day
        for piece_vector in reversed_pieces:
            current_play_row = self._grid[row]
            next_col = 0

            for item in piece_vector:
                if item == 1:
                    if self.is_unit_empty(unit_index=at + next_col, play_row=current_play_row):
                        current_play_row[at + next_col] = 'o'
                    else:
                        row += 1
                        self._current_play_row += 1
                        self.initialize_row()
                        self._grid.append(self._row)                        
                        current_play_row = self._row
                        current_play_row[at + next_col] = 'o'
                next_col += 1
                
                
            # piece_vector == [ 0, 1, 1 ]
            # board == [
            #             [ -, -, -, -, o, o, -, -, -, -, - ]
            #             [ -, -, -, -, -, -, -, -, -, -, - ]
            #          ]

            # Everything is just a scaler
            # self.position_emptiness_check_and_cause(current_row, position)


       
        # JUST NOTE:: the initial location could be empty where other
        # locations could be occupied.
        
        # if self._current_play_row > 0:
        #     current_row = self._current_play_row
        #     while True:


                
                
        #         for piece_value in piece_vector:
        #             xy = xy_position + piece_value
        #             if piece_value == 1:
        #                 pass


        #         is_empty, reason = self.position_emptiness_check_and_cause(current_row, xy_position)
        #         if is_empty:
        #             break


        # if self.position_emptiness_check_and_cause(xy_position):
        #     reversed_pieces = reversed(piece.space)
        #     for data in reversed_pieces:
        #         row_position = 0  # this is for a grid system
        #         col_position = 0
        #         for piece_value in data:
        #             xy = xy_position + col_position
        #             if piece_value == 1:
        #                 if self.is_unit_empty(xy):
        #                     self._row[xy] = 'o'
        #             col_position += 1
        # else:
            # self._grid.append(self._row)
            # self._current_play_row += 1
            # self.initialize_row()
            # self._grid.append(self._row)
            # self.place_piece(piece, xy_position)

    def is_unit_empty(self, unit_index:int, play_row:[]=None) -> bool:
        """Check if the given unit is empty.

        Args:
            unit_index (int): The index of the unit position in a grid.

        Returns:
            bool: True if the unit is empty.
        """
        if unit_index >= self._width:
            print(f'Unit {unit_index} is out of bounds. Cannot check if empty')
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
        print(self._grid)


if __name__ == '__main__':
    play_ground = PlayGround()
    l_piece = Piece([[1, 1, 1, 1]])
    i_piece = Piece(
        [
            [1],
            [1],
            [1],
            [1]
        ]
    )
    play_ground.place_piece(l_piece, 0)
    play_ground.place_piece(l_piece, 0)
    play_ground.place_piece(l_piece, 5)  # for case as this, the system needs to check the very first row to confirm it's fully taken
    play_ground.place_piece(i_piece, 4)
    play_ground.output_current_play_ground()

    
    

