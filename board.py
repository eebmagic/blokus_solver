from PIL import Image

class Board:
    size = 20
    spaces = []

    colors = {
                '0':(150, 150, 150),
                'y':(200, 150, 0),
                'r':(150, 0, 0),
                'g':(0, 100, 50),
                'b':(0, 0, 100)
            }


    def __init__(self):
        for y in range(self.size):
            row = []
            for x in range(self.size):
                row.append("0")
            self.spaces.append(row)

    
    def load(self, externalboard):
        self.spaces = externalboard


    def show(self):
        data = []
        for row in self.spaces:
            for point in row:
                data.append(self.colors[point])

        newim = Image.new("RGB", (self.size, self.size))
        newim.putdata(data)
        newim.show()