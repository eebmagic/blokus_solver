from PIL import Image

class Board:
    size = 20
    spaces = []

    colors = {
                '0':(250, 250, 250),
                'y':(225, 208, 47),
                'r':(224, 66, 63),
                'g':(9, 171, 89),
                'b':(50, 110, 200)
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
            for point in row.strip():
                data.append(self.colors[point])

        newim = Image.new("RGB", (self.size, self.size))
        newim.putdata(data)
        newim.show()