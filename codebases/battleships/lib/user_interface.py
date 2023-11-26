import copy
import sys

class UserInterface:
    def __init__(self, io, game):
        self.io = io
        self.game = game
        self.opponent_game = copy.deepcopy(game)

    def run(self):
        self._show("Welcome to the game!")
        games = {"Player 1": self.game, "Player 2": self.opponent_game}
        for player in ["Player 1", "Player 2"]:
            self._show(f"Set up {player}'s ships.")
            while len(games[player].unplaced_ships()) > 0:
                self._show(f"{player} has these ships remaining: " 
                        + f"{self._ships_unplaced_message(player)}")
                self._prompt_for_ship_placement(player)
                self._show(f"This is {player}'s board now:")
                self._show(self._format_board(player))
        # Ships are now set up.
        game_over = False
        while game_over == False:
            for player in ["Player 1", "Player 2"]:
                self._show(f"{player}'s turn to shoot.")
                self._prompt_for_shot(player)
                self._show(f"{player} has made these shots so far:")
                if player == "Player 1" and self._check_gameover() == False:
                    self._show(self._format_opponent_board(games["Player 2"]))
                elif player == "Player 2" and self._check_gameover() == False:
                    self._show(self._format_opponent_board(games["Player 1"]))
                else:
                    pass
                game_over = self._check_gameover()

        self._show(f"Player 1 {self.game.game_state}!")
        self._show(f"Player 2 {self.opponent_game.game_state}!")

    def _show(self, message):
        self.io.write(message + "\n")

    def _prompt(self, message):
        self.io.write(message + "\n")
        input = self.io.readline().strip()
        if input != "QUIT":
            return input
        else:
            exit()

    def _ships_unplaced_message(self, player):
        if player == "Player 1":
            game = self.game
        else:
            game = self.opponent_game
        ship_lengths = [str(ship.length) for ship in game.unplaced_ships()]
        return ", ".join(ship_lengths)

    def _prompt_for_ship_placement(self, player):
        ship_length = self._prompt("Which do you wish to place?")
        ship_orientation = self._prompt("Vertical or horizontal? [vh]")
        placement_is_valid = False
        while placement_is_valid == False:
            ship_row = self._prompt("Which row?")
            ship_col = self._prompt("Which column?")
            if player == "Player 1":
                game = self.game
            else:
                game = self.opponent_game
            try:
                game.place_ship(
                    length=int(ship_length),
                    orientation={"v": "vertical", "h": "horizontal"}[ship_orientation],
                    row=int(ship_row),
                    col=int(ship_col),
                )
                placement_is_valid = True
            except Exception as err:
                self._show(str(err))
        self._show("OK.")

    def _prompt_for_shot(self, player):
        if player == "Player 1":
            game = self.game
            nonplayer = "Player 2"
            nonplayer_game = self.opponent_game
        else:
            game = self.opponent_game
            nonplayer = "Player 1"
            nonplayer_game = self.game

        shot_is_valid = False
        while shot_is_valid == False:
            ship_row = self._prompt("Which row?")
            ship_col = self._prompt("Which column?")
            try:
                game.make_shot(int(ship_row), int(ship_col))
                shot_is_valid = True
            except Exception as err:
                self._show(str(err))
        
        hit_cache = sum(len(self.game.ships_placed[ship]["hits"]) \
                           for ship in self.game.ships_placed.keys())
        sunk_cache = [nonplayer_game.ships_placed[ship]["sunk"]
                    for ship in nonplayer_game.ships_placed.keys()].count(True)
        
        self.game.import_shots(self.opponent_game)
        self.opponent_game.import_shots(self.game)

        hits = sum(len(nonplayer_game.ships_placed[ship]["hits"]) \
                      for ship in nonplayer_game.ships_placed.keys())
        
        sunk = [self.game.ships_placed[ship]["sunk"] 
                for ship in self.game.ships_placed.keys()].count(True)

        if hits > hit_cache:
            self._show("That was a hit!")
        else:
            self._show("That was a miss!")
        
        if sunk > sunk_cache:
            self._show(f"{player} sank {nonplayer}'s ship!")

    def _format_board(self, player):
        if player == "Player 1":
            game = self.game
        else:
            game = self.opponent_game
        
        rows = []
        for row in range(1, game.rows + 1):
            row_cells = []
            for col in range(1, game.cols + 1):
                if game.ship_at(row, col):
                    row_cells.append("S")
                else:
                    row_cells.append(".")
            rows.append((row_cells))
        for shot in game.shots_received:
            rows[shot[0]-1][shot[1]-1] = \
                "X" if rows[shot[0]-1][shot[1]-1] == "S" else "O"
        board_rows = []
        for row_cells in rows:
            board_rows.append("".join(row_cells))
        return "\n".join(board_rows)

    def _format_opponent_board(self, opponent_game):
        rows = []
        for row in range(1, opponent_game.rows + 1):
            row_cells = []
            for col in range(1, opponent_game.cols + 1):
                row_cells.append(".")
            rows.append((row_cells))
        for shot in opponent_game.shots_received:
            rows[shot[0]-1][shot[1]-1] = \
                "X" if any(shot in opponent_game.ships_placed[ship]["position"] for ship in opponent_game.ships_placed.keys()) else "O"
        board_rows = []
        for row_cells in rows:
            board_rows.append("".join(row_cells))
        return "\n".join(board_rows)
    
    def _check_gameover(self):
        self.game.import_shots(self.opponent_game)
        self.opponent_game.import_shots(self.game)
        if (self.game.game_state, self.opponent_game.game_state) != ("playing", "playing"):
            return True
        else:
            return False