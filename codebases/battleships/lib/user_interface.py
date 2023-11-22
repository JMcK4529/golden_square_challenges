class UserInterface:
    def __init__(self, io, game):
        self.io = io
        self.game = game

    def run(self):
        self._show("Welcome to the game!")
        self._show("Set up your ships first.")
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
