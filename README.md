# Blokus Solver
A solver for boards from the game [Blokus](https://en.wikipedia.org/wiki/Blokus).

1. User takes an image of the board and feed it into the program
2. Processes the image into a 20x20 grid game board object (hopefully filled in with valid pieces)
3. Determines which pieces a player has left
4. Determines which piece + position would be the best move for a player
5. Displays that optimal move back to the user visually

# File Guide:

## General:
### board.py
Has code for Board object. Used in varrying cases.

## Building:
### build_board.py
Pulls together all building components in order to build a Board object from an image file. (Only has one function)

### round_image.py
Some misc functions for smoothing images and converting them to color palletes.

### trimmer.py
Main function full_clean(image, value) trims an image given the background color (value).

### analyze.py
Some misc functions for collecting data about an image or performing small manipulations.
- round_pixel
- color_counts
- find_board_color
- average_color
- make_boardstring


