

class City:

    def __init__(self, x, y, no):
        self.x = x
        self.y = y
        self.id = no

    def distance(self, city):
        distance = ((self.x - city.x)**2 + (self.y - city.y)**2)**(1/2)
        return distance
