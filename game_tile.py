

class GameTile(object):
    def __init__(self, column, row):
        self.row = row
        self.column = column
        self.construct = None

    def __lt__(self, other):
        return False

    def is_occupied(self):
        if not self.construct:
            return False
        return True
