import pytest
import unittest
from lib.game import *
from lib.ship_placement import *
from lib.ship import *
from lib.user_interface import *
from tests.terminal_interface_helper_mock import TerminalInterfaceHelperMock

def test_game_place_ship_constraint_to_board():
    board_size_range = zip(range(5, 16), range(5, 16))
    for size in board_size_range:
        rows, cols = size
        game = Game(rows, cols)
        for orientation in ("horizontal", "vertical"):
            for length in range(2,6):
                for col in [0] + list(range(cols - length + 1, cols + 1)):
                    row = 5
                    if orientation == "vertical":
                        row, col = col, row
                    with pytest.raises(Exception) as err:
                        game.place_ship(length, orientation, row, col)
                    assert str(err.value) == "Ship overlaps board edge"

def test_game_place_ship_constraint_no_overlap():
    pass

class TestUserInterface(unittest.TestCase):
    def test_ships_constrained_to_board_in_interface(self):
        game = Game()
        ship_choices = [str(ship) for ship in list(range(2,6))]
        orient_choices = ["h", "v"]
        
        for ship_choice in ship_choices:
            for orient_choice in orient_choices:
                first_row_choices = [str(row) for row in list(range(1, 11))]
                first_col_choices = [str(col) for col in [0] + list(range(11 - int(ship_choice), 11))]
                second_col_choices = [str(col) for col in list(range(1, 11 - int(ship_choice)))]
                print(first_row_choices)
                for row_choice in first_row_choices:
                    for col_choice in first_col_choices:
                        for col_choice_2 in second_col_choices:
                            row_choice_2 = row_choice

                            #print(row_choice, ":", col_choice, "\n", row_choice_2, ":", col_choice_2)
                            #if orient_choice == "v":
                            #    row_choice, row_choice_2, col_choice, col_choice_2 = col_choice, col_choice_2, row_choice, row_choice_2
                            
                            print("before build")
                            print(orient_choice,row_choice_2,col_choice_2)
                            game_board_builder = Game()
                            if orient_choice == "h":
                                build_row, build_col, build_orient = int(row_choice_2), int(col_choice_2), "horizontal"
                            else:
                                build_col, build_row, build_orient = int(row_choice_2), int(col_choice_2), "vertical"
                            game_board_builder.place_ship(int(ship_choice), build_orient, build_row, build_col)
                            print("after build place")
                            expected_board_state = []
                            for row in range(1, game_board_builder.rows + 1):
                                cells = []
                                for col in range(1, game_board_builder.cols + 1):
                                    if game_board_builder.ship_at(row, col):
                                        cells.append("S")
                                    else:
                                        cells.append(".")
                                expected_board_state.append("".join(cells))
                            expected_board_state = "\n".join(expected_board_state)
                            game_board_builder = Game()
                            game = Game()
                            print(f"Ship: {ship_choice}\nChoice 1: {orient_choice}({row_choice}, {col_choice})\nChoice 2: {orient_choice}({row_choice_2}, {col_choice_2})")
                            
                            io = TerminalInterfaceHelperMock()
                            interface = UserInterface(io, game)
                            io.expect_print("Welcome to the game!")
                            io.expect_print("Set up your ships first.")
                            io.expect_print("You have these ships remaining: 2, 3, 3, 4, 5")
                            io.expect_print("Which do you wish to place?")
                            io.provide(ship_choice)
                            io.expect_print("Vertical or horizontal? [vh]")
                            io.provide(orient_choice)
                            io.expect_print("Which row?")
                            io.provide(row_choice if orient_choice == "h" else col_choice)
                            io.expect_print("Which column?")
                            io.provide(col_choice if orient_choice == "h" else row_choice)
                            io.expect_print("Oops! That ship overlaps the board edge!")
                            io.expect_print("Which row?")
                            io.provide(row_choice_2 if orient_choice == "h" else col_choice_2)
                            io.expect_print("Which column?")
                            io.provide(col_choice_2 if orient_choice == "h" else row_choice_2)
                            io.expect_print("OK.")
                            io.expect_print("This is your board now:")
                            io.expect_print(expected_board_state)
                            io.expect_print("Done, for now!")
                            interface.run()
