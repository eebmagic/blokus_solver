from PIL import Image

class Board:
    size = 20
    spaces = []

    # Color definitions for making image
    colors = {
                '0' : (250, 250, 250),
                'y' : (225, 208, 47),
                'r' : (224, 66, 63),
                'g' : (9, 171, 89),
                'b' : (50, 110, 200)
            }


    def __init__(self):
        '''
        default spaces for a board object is all empty spaces
        '''
        for y in range(self.size):
            row = []
            for x in range(self.size):
                row.append("0")
            self.spaces.append(row)


    def __str__(self):
        return '\n'.join([''.join(row) for row in self.spaces])

    
    def load(self, externalboard):
        '''
        Functions as a setter for the spaces string
        '''
        if type(externalboard) == str:
            out = []
            rows = externalboard.split('\n')
            for row in rows:
                out.append([char for char in row])
            self.spaces = out

        elif type(externalboard) == list:
            self.spaces = externalboard


    def show(self, title='BOARD'):
        '''
        Builds a PIL image object from image data and then shows it
        '''
        data = []
        for row in self.spaces:
            for point in row:
                data.append(self.colors[point])

        newim = Image.new("RGB", (self.size, self.size))
        newim.putdata(data)
        newim.show(title=title)


'''
# Code for testing:
if __name__ == '__main__':
    outstring = 'ggg00ggg0bbbbrrr0rry\ng00gg0gg0bggggrrbbr0\ngr0gg000ggbbbgbbrbr0\nrgrrrg0g0rrbrbbrrr00\nrgyyyggg0rrbrrr0r0rr\nrgy0gyy0g00rbbr0g00r\nrgygggygg00rrbbgg0rr\n0rryg0yy0ggrg0bg0g00\nrryrrr00ggrggg0bbggg\n0yy00rr0grr00g0bbg00\nyy00yyyrrg0rrrgggbb0\nrryy00rrbbgr00b00b00\nr0ryyyr0bbgr0bbb0bb0\nryrrrryybgg000byb00b\n0yy000yy0bbbbyyybb0b\n0y00y0y0yyy0yb0yb0bb\ny00yyy00y0ybybbbyyb0\nyyy0y0bbbbbybyy0ybyy\n000ybb0y0yyybbyy0byy\nyyyy0yyyy0ybb0000bbb'
    b = Board()
    b.load(outstring)
    b.show()
    print('b = ', b)
'''
