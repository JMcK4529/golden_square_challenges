from lib.ship import Ship
from lib.ship_placement import ShipPlacement
import copy


class Game:
    def __init__(self, rows=10, cols=10, ships=[Ship(2),Ship(3),Ship(3),Ship(4),Ship(5)]):
        self.rows = rows
        self.cols = cols
        self.ship_placements = []
        self.ships_placed = {}
        self.ships_unplaced = ships.copy()
        self.shots_made = []
        self.shots_received = None
        self.game_state = "playing"

    def unplaced_ships(self):
        return self.ships_unplaced

    def place_ship(self, length, orientation, row, col):
        if row <= 0 or col <= 0 \
            or (orientation == "horizontal" and col + length - 1 > self.cols) \
                or (orientation == "vertical" and row + length - 1 > self.rows):
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
            ship_placement = ShipPlacement(
                length=length,
                orientation=orientation,
                row=row,
                col=col,
            )
            self.ship_placements.append(ship_placement)
            
            position = []
            if orientation == "horizontal":
                for pos_col in range(col, col + length):
                    position.append((row, pos_col))
            else:
                for pos_row in range(row, row + length):
                    position.append((pos_row, col))

            placed = False
            i = 0
            while placed == False:
                if self.ships_unplaced[i].length == length:
                    self.ships_placed.update(
                        {
                        self.ships_unplaced.pop(i).length: {
                            "position": position, "hits": [], "sunk": False
                            }
                        }
                    )
                    placed = True
                else:
                    i += 1
            
    def ship_at(self, row, col):
        for ship_placement in self.ship_placements:
            if ship_placement.covers(row, col):
                return True
        return False

    def make_shot(self, row, col):
        if row <= 0 or row > self.rows or col <= 0 or col > self.cols:
            raise Exception("Oops! That shot missed the board!")
        else:
            self.shots_made.append((row, col))

    def import_shots(self, opponent_game):
        self.shots_received = opponent_game.shots_made
        for shot in self.shots_received:
            for ship_length in self.ships_placed.keys():
                if shot in self.ships_placed[ship_length]["position"]:
                    self.ships_placed[ship_length]["hits"].append(shot)
                if set(self.ships_placed[ship_length]["position"]) == \
                                set(self.ships_placed[ship_length]["hits"]):
                    self.ships_placed[ship_length]["sunk"] = True
        if all([self.ships_placed[length]["sunk"] for length in self.ships_placed.keys()]):
            self.game_state = "lost"