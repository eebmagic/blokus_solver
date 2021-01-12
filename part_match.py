import numpy as np

def list_from_string(piece):
    '''
    Convert a newline-separated string into a 2-dimensional char list
    '''
    out = []
    for row in piece.split('\n'):
        out.append([char for char in row])

    return out


def string_from_list(charList):
    '''
    Convert a list of chars into a newline-separated string.
    '''
    rows = [''.join(x) for x in charList]
    return '\n'.join(rows)


def boolean_list(charList):
    '''
    Convert a char list of ('0', 'x') to (False, True)
    '''
    out = []
    for row in charList:
        new = []
        for char in row:
            new.append(char == 'x')
        out.append(new)

    return out


def place(board, piece, x=0, y=0, verbose=False):
    '''
    Replace values in a board with values in a piece matrix
    board: the numpy matrix to start with
    piece: the smaller numpy matrix to get values from, which replace those in the board
    x, y: the position on 
    '''
    if verbose:
        print(f'\n{piece.shape = }')
        print(f'position: {x, y}')
        print(piece)
        print(f'{board.shape = }')

    assert x >= 0 and x <= board.shape[0], "x must be >= 0 and <= board width"
    assert y >= 0 and y <= board.shape[1], f"y must be >= 0 and <= board height"
    assert type(piece) == np.ndarray, "Piece must be numpy array"
    assert type(board) == np.ndarray, "Board must be numpy array"
    y_shape_msg = f"Piece y size can't be larger than the board ({y=}, height={board.shape[1]})"
    x_shape_msg = f"Piece x size can't be larger than the board (widths: piece={piece.shape[0]}, board={board.shape[0]})"
    assert piece.shape[1] <= board.shape[1], y_shape_msg
    assert piece.shape[0] <= board.shape[0], x_shape_msg
    y_position_msg = f"y can't place the piece outside of the board ({y=}, pieceHeight={piece.shape[0]}, boardHeight={board.shape[0]})"
    x_position_msg = f"x can't place the piece outside of the board ({x=}, pieceHeight={piece.shape[1]}, boardHeight={board.shape[1]})"
    assert y + piece.shape[0] <= board.shape[0], y_position_msg
    assert x + piece.shape[1] <= board.shape[1], x_position_msg

    out = board.copy()
    out[y:y + piece.shape[0], x:x + piece.shape[1]] += piece
    return out


def orientations(piece):
    '''
    Given a string representation of a piece,
    return all possible orientations of the piece.
    Return orientations as char lists.
    '''

    # Add base 4 orientations
    out = [list_from_string(piece)]
    for i in range(3):
        new = np.rot90(np.array(out[-1])).tolist()
        if new not in out:
            out.append(new)

    # Repeat for flipped version of piece if necesssary
    flipped = np.flip(np.array(out[0]), 1).tolist()
    if flipped not in out:
        out.append(flipped)
        for i in range(3):
            new = np.rot90(np.array(out[-1])).tolist()
            if new not in out:
                out.append(new)

    return out


def all_pieces():
    '''
    Returns all pieces (only a sinlge orientation per piece).
    Returns pieces as a list of '0'/'x' strings
    '''
    with open('pieces.txt') as file:
        content = file.read().strip()
        pieces = content.split('\n\n')

    return pieces


def all_piece_orientations():
    '''
    Returns all pieces and all possible rotations/flips.
    Returns pieces as a list of '0'/'x' strings
    '''
    out = []
    for piece in all_pieces():
        for orientation in orientations(piece):
            out.append(string_from_list(orientation))

    return out


def expand_mask(mask):
    '''
    Turns a boolean piece mask into one that includes
    the piece and all surrounding positions.
    NOTE: This does not include diagonal directions,
          so this can be used to verify valid plays.
    NOTE: The mask should already be the same shape of the board
    '''
    out = mask.copy()
    adjusts = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for y in range(len(out)):
        for x in range(len(out[0])):
            for x_adj, y_adj in adjusts:
                x_real = x + x_adj
                y_real = y + y_adj

                if x_real >= 0 and x_real < len(out[0]):
                    if y_real >= 0 and y_real < len(out):
                        if mask[y_real][x_real]:
                            out[y][x] = True

    return out


def diagonal_mask(mask, verbose=False):
    '''
    Turns a boolean piece mask into one that only
    includes the diagonal connections.
    Used to verify valid plays.
    NOTE: The mask should already be the shape of the board.
    '''
    out = np.full(mask.shape, False)
    diagonals = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for y in range(len(out)):
        for x in range(len(out[0])):
            total = 0
            for x_adj, y_adj in neighbors:
                x_real = x + x_adj
                y_real = y + y_adj
                if x_real >= 0 and x_real < len(out[0]):
                    if y_real >= 0 and y_real < len(out):
                        if mask[y_real][x_real]:
                            total -= 1

            if total >= 0:
                for x_adj, y_adj in diagonals:
                    x_real = x + x_adj
                    y_real = y + y_adj
                    if x_real >= 0 and x_real < len(out[0]):
                        if y_real >= 0 and y_real < len(out):
                            if mask[y_real][x_real]:
                                out[y][x] = True

    if verbose:
        print('Original:')
        print(string_from_list(np.where(mask, 'x', '0').tolist()))
        print('Generated:')
        print(string_from_list(np.where(out, 'x', '0').tolist()))

    return out


def check_surroundings(boardString, pieceOrientationString, position, verbose=False):
    '''
    Returns the counts for the colors under and around a piece at a given position.

    boardString: str of the board spaces
    peiceOrientationString: the '0'/'x' str of the piece in the target orientation
    position: the (x, y) position to place the piece on the board
    verbose: optional param for printouts
    '''
    piece = np.array(boolean_list(list_from_string(pieceOrientationString)))
    board = np.array(list_from_string(boardString))
    x, y = position

    mask = place(np.full(board.shape, False), piece, x=x, y=y)
    expanded = expand_mask(mask)

    piece_result = board[mask]
    expanded_result = board[expanded]

    # Check contents of results all same value
    unique, counts = np.unique(piece_result, return_counts=True)
    original_counts = dict(zip(unique, counts))
    unique, counts = np.unique(expanded_result, return_counts=True)
    expanded_counts = dict(zip(unique, counts))

    if verbose:
        print('\nVerbose output from check_surroundings():')
        print('Mask:')
        print(mask)
        print(original_counts)
        print('Expanded:')
        print(expanded)
        print(expanded_counts)

    return expanded_counts


def check_diagonal_surroundings(boardString, pieceOrientationString, position, verbose=False):
    piece = np.array(boolean_list(list_from_string(pieceOrientationString)))
    board = np.array(list_from_string(boardString))
    x, y = position

    if verbose:
        print('Placing:')
        print(piece)
        print('Inside board:')
        for i in str(board.tolist()).split('],'):
            print(i)
        print('At position: ', position)

    mask = place(np.full(board.shape, False), piece, x=x, y=x)
    diagonals = diagonal_mask(mask)

    diagonal_result = board[diagonals]

    unique, counts = np.unique(diagonal_result, return_counts=True)
    diagonal_counts = dict(zip(unique, counts))

    return diagonal_counts


def find_positions(board, piece, verbose=False):
    '''
    Given a piece, find all positions the piece can possibly be placed in
    for each possible orientation of the piece.
    board: str, rectangular representation of the board to work with ('r'/'g'/'b'/'y': piece part, '0': emtpy space)
    piece: str, rectangular representation of the piece ('x': part of piece, '0': empty space in rect)
           piece is attemtped to be placed in all possible orientations
    Piece must be smaller (along x and y axis) than the board.

    Should return a dictionary of char -> positions where piece fits on those chars.
    For example out['0'] would be all free spaces where the piece can fit,
    '''

    # Run checks on params
    assert type(board) == str, 'Board must be passed as as string'
    assert type(piece) == str, 'Piece must be passed as as string'
    board_list = list_from_string(board)
    piece_list = list_from_string(piece)
    x_valid = len(board_list) >= len(piece_list)
    y_valid = len(board[0]) >= len(piece[0])
    assert x_valid and y_valid, 'Board must be <= size of piece along each axis'

    # Get all possible piece orientations (as Boolean masks)
    ors = orientations(piece)
    masks = [np.array(boolean_list(orientation)) for orientation in ors]

    # Make board into np array
    board_arr = np.array(list_from_string(board))

    if verbose:
        print("Here's the numpy array for the board:")
        print(board_arr)
        print("\nHere's the piece:")
        print(piece)
        print("\nHere's a mask for the piece:")
        print(masks[0])

    output = {}

    # March masks across the board to check all valid positions
    for mask_ind, mask in enumerate(masks):
        x_stop = board_arr.shape[1] - mask.shape[1]
        y_stop = board_arr.shape[0] - mask.shape[0]
        for x in range(0, x_stop):
            for y in range(0, y_stop):
                position = (x, y)

                # Make the piece matrix the same size as board, adjusted by x, y
                piece_mask = place(np.full(board_arr.shape, False), mask, x=x, y=y)

                # Mask full piece matrix with board
                result = board_arr[piece_mask]

                # Check contents of results all same value
                unique, counts = np.unique(result, return_counts=True)
                counts = dict(zip(unique, counts))

                if len(counts) == 1:
                    existing_value = list(counts.keys())[0]
                    orientation = string_from_list(ors[mask_ind])
                        
                    # Verify that position holds true given surroundings (if not an empty space)
                    valid_placement = True
                    if existing_value != '0':
                        surrounding_counts = check_surroundings(board, orientation, position)
                        if counts[existing_value] != surrounding_counts[existing_value]:
                            valid_placement = False

                    if verbose and valid_placement:
                        print(f"\nHere's the piece mask ({x}, {y}):")
                        print(piece_mask)
                        print(board_arr)
                        print(result)
                        print(f"Position: {position}")
                        print(f'{existing_value = }')
                        print('orientation:')
                        print(orientation)

                    if valid_placement:
                        entry = (position, orientation)
                        if existing_value in output:
                            output[existing_value].append(entry)
                        else:
                            output[existing_value] = [entry]
                else:
                    # print(f'({position}) WAS NOT a valid position')
                    # print(f"ERROR ({position}) Counts:")
                    # print(counts)
                    if verbose:
                        print(f"\nHere's the piece mask ({x}, {y}):")
                        print(piece_mask)
                        print(board_arr)
                        print(result)
                        print(f"Position: {position}")
                        print(f'{existing_value = }')
                        print('orientation:')
                        print(orientation)

    return output



if __name__ == '__main__':
    with open('pieces.txt') as file:
        content = file.read().strip()
        pieces = content.split('\n\n')

    with open('example_board.txt') as file:
        board_string = file.read().strip()


    # x = list_from_string(pieces[0])
    # x = pieces[7]
    # out = find_positions(board_string, x, verbose=False)
    # print('\nFinished Output:')
    # print(out)
    # print(board_string)
    # print("")

    # for pos, orientaiton in out['0']:
    #     print(pos)
    #     print(orientaiton)
    #     print("")

    from board import Board
    b = Board()
    with open('example_boards/transcriptions/three.txt') as file:
        content = file.read().strip()
        b.load(content)

    piece = all_pieces()[0]
    out = find_positions(str(b), piece, verbose=True)

    print("Piece:")
    print(piece)
    print(out)

    # for piece in pieces:
    #     rots = orientations(piece)
    #     print(f'\n{len(rots)} - {piece = }')
    #     for rotation in rots:
    #         print(f'{rotation}')
    #         print('----')
    #         print(string_from_list(rotation))
    #         print('----')
    #         print('\n')
