from lib.ship import Ship
from lib.ship_placement import ShipPlacement


class Game:
    def __init__(self, rows=10, cols=10):
        self.ships_placed = []
        self.rows = rows
        self.cols = cols

    def unplaced_ships(self):
        return [
            Ship(2),
            Ship(3),
            Ship(3),
            Ship(4),
            Ship(5),
        ]

    def place_ship(self, length, orientation, row, col):
        if row <= 0 or col <= 0 \
        or (orientation == "horizontal" and col + length > self.cols) \
        or (orientation == "vertical" and row + length > self.rows):
            raise Exception("Ship overlaps board edge")
        elif orientation == "horizontal" and \
                                        any(
                                            [self.ship_at(row, check_col) 
                                            for check_col
                                            in range(col, col + length)]
                                            ):
            raise Exception("Ship overlaps a previously placed ship")
        elif orientation == "vertical" and \
                                        any(
                                            [self.ship_at(check_row, col)
                                            for check_row
                                            in range(row, row + length)]
                                            ):
            raise Exception("Ship overlaps a previously placed ship")
        else:
            print(any([self.ship_at(row, check_col) for check_col in range(col, col + length + 1)]))
            print(any([self.ship_at(col, check_row) for check_row in range(col, col + length + 1)]))
            ship_placement = ShipPlacement(
                length=length,
                orientation=orientation,
                row=row,
                col=col,
            )
            self.ships_placed.append(ship_placement)

    def ship_at(self, row, col):
        for ship_placement in self.ships_placed:
            if ship_placement.covers(row, col):
                return True
        return False
