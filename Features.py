#bullet class
class Bullet:
    def __init__(self, coordinates, vector, sprite):
        self.coordinates = list(coordinates)
        self.height = 10
        self.width = 10
        self.velocity = 10 * vector
        self.sprite = sprite        

