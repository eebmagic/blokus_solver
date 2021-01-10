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


def place(board, piece, x=0, y=0):
    assert x >= 0 and x <= board.shape[1], "x must be >= 0 and <= board width"
    assert y >= 0 and y <= board.shape[0], f"y must be >= 0 and <= board height"
    assert type(piece) == np.ndarray, "Piece must be numpy array"
    assert type(board) == np.ndarray, "Board must be numpy array"
    assert piece.shape[0] <= board.shape[0], "Piece x size can't be larger than the board"
    assert piece.shape[1] <= board.shape[1], "Piece y size can't be larger than the board"
    assert y + piece.shape[0] <= board.shape[0], "y can't place the piece outside of the board"
    assert x + piece.shape[1] <= board.shape[1], "x can't place the piece outside of the board"

    out = board
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

    TODO: Maybe need another function to identify valid existing pieces on the board?
    Could also check for invalid pieces to verify board recognition.

    TODO: Add check for piece color with player color on board for valid plays?
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
        print("\nHere's a mask:")
        print(masks[0])
        print("\nAnd another:")
        print(masks[-1])
        print(type(masks[0]))

    output = {}

    # March masks across the board to check all valid positions
    for mask_ind, mask in enumerate(masks):
        for x in range(0, board_arr.shape[1] - mask.shape[1] + 1):
            for y in range(0, board_arr.shape[0] - mask.shape[0] + 1):
                position = (x, y)

                # TODO: Fill this in
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

                    if verbose:
                        print(f"\nHere's the piece mask ({x}, {y}):")
                        print(piece_mask)
                        print(board_arr)
                        print(f"Position: {position}")
                        print(f'{existing_value = }')
                        print('orientation:')
                        print(orientation)

                    entry = (position, orientation)
                    if existing_value in output:
                        output[existing_value].append(entry)
                    else:
                        output[existing_value] = [entry]

    return output



if __name__ == '__main__':
    with open('pieces.txt') as file:
        content = file.read().strip()
        pieces = content.split('\n\n')

    with open('example_board.txt') as file:
        board_string = file.read().strip()


    # x = list_from_string(pieces[0])
    x = pieces[7]
    out = find_positions(board_string, x, verbose=False)
    print(out)

    print(board_string)
    print("")

    for pos, orientaiton in out['0']:
        print(pos)
        print(orientaiton)
        print("")


    # for piece in pieces:
    #     rots = orientations(piece)
    #     print(f'\n{len(rots)} - {piece = }')
    #     for rotation in rots:
    #         print(f'{rotation}')
    #         print('----')
    #         print(string_from_list(rotation))
    #         print('----')
    #         print('\n')
