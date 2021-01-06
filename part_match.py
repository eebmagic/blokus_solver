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


def find_positions(board, piece):
    '''
    Given a piece, find all positions the piece can be placed in
    for each possible orientation of the piece.
    Board and piece should be passed as strings.
    Piece must be smaller (along x and y axis) than the board.

    Should return a dictionary of char -> positions where piece fits on those chars.
    For example out['0'] would be all free spaces where the piece can fit,

    TODO: Maybe need another function to identify valid existing pieces on the board?
    Could also check for invalid pieces to verify board recognition.
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
    # print(f'Original:\n{piece}\n')
    # for mask in masks:
    #     print(f'Heres a mask:\n{mask}\n')


    # Make board into np array
    board_arr = np.array(list_from_string(board))
    print("Here's the numpy array for the board:")
    print(board_arr)

    print("\nHere's the piece:")
    print(piece)

    # March masks across the board to check all valid positions
    for x in range(0, len(board_list) - len(piece_list)):
        for y in range(0, len(board_list[0]) - len(piece_list[0])):
            pass
            # TODO: Fill this in



if __name__ == '__main__':
    with open('pieces.txt') as file:
        content = file.read().strip()
        pieces = content.split('\n\n')

    with open('example_board.txt') as file:
        board_string = file.read().strip()


    # x = list_from_string(pieces[0])
    x = pieces[7]
    find_positions(board_string, x)


    # for piece in pieces:
    #     # flip(piece)

    #     rots = orientations(piece)
    #     print(f'\n{len(rots)} - {piece = }')
    #     for rotation in rots:
    #         # print(f'{rotation}')
    #         print('----')
    #         print(string_from_list(rotation))
    #         print('----')
    #         print('\n')
