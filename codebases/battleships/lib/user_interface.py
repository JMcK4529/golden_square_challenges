import copy

class UserInterface:
    def __init__(self, io, game):
        self.io = io
        self.game = game
        self.opponent_game = copy.copy(game)

    def run(self):
        self._show("Welcome to the game!")
        self._show("Set up your ships first.")
        while len(self.game.unplaced_ships()) > 0:
            self._show("You have these ships remaining: {}".format(
                self._ships_unplaced_message()))
            self._prompt_for_ship_placement()
            self._show("This is your board now:")
            self._show(self._format_board())

    def _show(self, message):
        self.io.write(message + "\n")

    def _prompt(self, message):
        self.io.write(message + "\n")
        return self.io.readline().strip()

    def _ships_unplaced_message(self):
        ship_lengths = [str(ship.length) for ship in self.game.unplaced_ships()]
        return ", ".join(ship_lengths)

    def _prompt_for_ship_placement(self):
        ship_length = self._prompt("Which do you wish to place?")
        ship_orientation = self._prompt("Vertical or horizontal? [vh]")
        placement_is_valid = False
        while placement_is_valid == False:
            ship_row = self._prompt("Which row?")
            ship_col = self._prompt("Which column?")
            try:
                self.game.place_ship(
                    length=int(ship_length),
                    orientation={"v": "vertical", "h": "horizontal"}[ship_orientation],
                    row=int(ship_row),
                    col=int(ship_col),
                )
                placement_is_valid = True
            except:
                self._show("Oops! That ship overlaps the board edge!")
        self._show("OK.")

    def _format_board(self):
        rows = []
        for row in range(1, self.game.rows + 1):
            row_cells = []
            for col in range(1, self.game.cols + 1):
                if self.game.ship_at(row, col):
                    row_cells.append("S")
                else:
                    row_cells.append(".")
            rows.append("".join(row_cells))
        return "\n".join(rows)
    
    def generate_opponent_board(self):
        for args in zip([2,3,3,4,5],
                        ["horizontal","horizontal",
                         "vertical","horizontal",
                         "vertical"],
                         [2,3,4,8,1], 
                         [2,3,6,2,10]):
            self.opponent_game.place_ship(args[0], args[1], args[2], args[3])
