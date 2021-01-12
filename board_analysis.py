from part_match import find_positions
from part_match import all_pieces
from part_match import check_surroundings
from part_match import check_diagonal_surroundings

def sort_fn(piece):
    '''
    Sort by most number of squares, multiplied by the area of the piece.
    '''
    assert type(piece) == str, 'piece must be passed as a string'
    splits = piece.split('\n')
    return piece.count('x') * len(splits) * len(splits[0])


def find_best_play(boardString, playerColor, verbose=False):
    '''
    Find the set of pieces for each color that appear on the board.

    boardString: The string representation of the board
    playerColor: The color for the player's pieces ('r', 'g', 'b', 'y')

    Returns: (best piece as written in definition,
        (x, y) position to play,
        orientation to play the piece)

    TODO: Determine if there are any illegitimate pieces?
    '''
    assert type(boardString) == str, 'Board must be passed as a string'
    pieces = all_pieces()

    # Keep track of pieces that each player hasn't played
    colors = ['r', 'g', 'b', 'y']
    unplayed_pieces = {}
    for color in colors:
        unplayed_pieces[color] = pieces.copy()

    # Keep track of all positions that each piece could be played in
    print('Finding positions for each piece...')
    available_positions = {}
    for piece in pieces:
        positions = find_positions(boardString, piece, verbose=False)

        # Remove pieces played by each player
        for color in colors:
            if color in positions:
                unplayed_pieces[color].remove(piece)

        # Keep track of piece-shaped gaps
        if '0' in positions:
            available_positions[piece] = positions['0']

    player_pieces = unplayed_pieces[playerColor]


    no_pieces_msg = f'Player: {playerColor} has no pieces left to play'
    assert len(player_pieces) != 0, no_pieces_msg

    player_pieces = sorted(player_pieces, key=sort_fn, reverse=True)

    if verbose:
        for piece in available_positions:
            print(piece)
            print(available_positions[piece])
            print(len(available_positions[piece]))
            print('')

        print("Player's pieces:")
        for ind, piece in enumerate(player_pieces):
            print(piece)
            print(ind)
            print()

    positions = 0
    output_position = None
    output_orientation = None
    output_piece = None
    for piece in player_pieces:
        if piece in available_positions:
            positions = len(available_positions[piece])
            if verbose:
                print('\nTrying for piece:')
                print(piece)
                print(f'Total available spaces for piece: {positions}')
                print(available_positions[piece])

            valid_found = False
            for spot_position, spot_orientation in available_positions[piece]:
                valid_play = check_valid_play(boardString, spot_orientation, spot_position, playerColor)
                if verbose:
                    print('')
                    print(spot_position)
                    print(spot_orientation)
                    print(f'{valid_play = }')
                if valid_play:
                    valid_found = True
                    output_orientation = spot_orientation
                    output_position = spot_position
                    output_piece = piece
                    break
            if valid_found:
                break

    return (output_piece, output_position, output_orientation)


def check_valid_play(boardString, pieceOrientationString, position, playerColor):
    surrounding_counts = check_surroundings(boardString, pieceOrientationString, position)
    if playerColor in surrounding_counts:
        neighboring_blocks = surrounding_counts[playerColor]
    else:
        neighboring_blocks = 0

    diagonals = check_diagonal_surroundings(boardString, pieceOrientationString, position)
    if playerColor in diagonals:
        diagonal_blocks = diagonals[playerColor]
    else:
        diagonal_blocks = 0

    return neighboring_blocks == 0 and diagonal_blocks > 0


if __name__ == '__main__':
    from board import Board
    b = Board()
    with open('example_boards/transcriptions/three.txt') as file:
        content = file.read().strip()
        b.load(content)

    player_color = 'r'
    piece, position, orientation = find_best_play(str(b), player_color)
    print(position)
    print(orientation)

    # Graph to user
    from part_match import *
    piece = np.array(boolean_list(list_from_string(orientation)))
    mask = place(np.full((20, 20), False), piece, x=position[0], y=position[1])
    b.highlight(player_color, mask)
    # b.show()
