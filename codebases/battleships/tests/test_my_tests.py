import pytest
import unittest
import copy
from lib.game import *
from lib.ship_placement import *
from lib.ship import *
from lib.user_interface import *
from tests.terminal_interface_helper_mock import TerminalInterfaceHelperMock

#@pytest.mark.skip(reason="")
def test_game_place_ship_constraint_to_board():
    board_size_range = range(5,16)
    board_sizes = zip(board_size_range, board_size_range)
    for size in board_sizes:
        rows, cols = size
        game = Game(rows, cols)

        """
        Raise Exceptions when ships placed outside valid range.
        """
        for orientation in ("horizontal", "vertical"):
            for length in range(2,6):
                for col in [0] + list(range(cols - length + 2, cols + 1)):
                    row = 5
                    if orientation == "vertical":
                        row, col = col, row
                    with pytest.raises(Exception) as err:
                        ## debug
                        # print("deliberate fail: ", size, length, orientation, row, col)
                        game.place_ship(length, orientation, row, col)
                    assert str(err.value) == "Ship overlaps board edge"
                
                """
                Raise no Exceptions for ships placed within valid range.
                """
                for col in range(1, cols - length + 2):
                    row = 5
                    if orientation == "vertical":
                        row, col = col, row
                    ## debug
                    # print("pass: ", size, length, orientation, row, col)
                    game.place_ship(length, orientation, row, col)
                    game = Game(rows, cols)

#@pytest.mark.skip(reason="")
def test_game_place_ship_constraint_no_overlapping_ships():    
    """
    Horizontal obstacle, vertical ship placement
    """
    game_list = []
    placement_list = []
    game_rows = 10
    game_cols = 10
    obs_orient = "horizontal"
    for obs_length in range(2, 6):
        for obs_row in range(1, 11):
            for obs_col in range(1, game_cols - obs_length):
                game = Game(game_rows, game_cols)
                game.place_ship(obs_length, obs_orient, obs_row, obs_col)
                print(game.ships_unplaced, "\n", (obs_length, obs_orient, obs_row, obs_col))
                game_list.append(game)
                placement_list.append({"len": obs_length, "ori": obs_orient, "row": obs_row, "col": obs_col})
    
    ship_orient = "vertical"
    for game, obstacle in zip(game_list, placement_list):
        game_cache = copy.copy(game)
        for ship_length in range(2, 6):
            for ship_row in range(max(obstacle["row"] - ship_length + 1, 1), min(obstacle["row"], game_rows - ship_length + 1)):
                for ship_col in range(obstacle["col"], obstacle["col"] + obstacle["len"]):
                    len = obstacle["len"]
                    row = obstacle["row"]
                    col = obstacle["col"]
                    ori = obstacle["ori"]
                    ## debug
                    # print(len, ori, row, col, "\n", ship_length, ship_orient, ship_row, ship_col)
                    with pytest.raises(Exception) as err:
                        game.place_ship(ship_length, ship_orient, ship_row, ship_col)
                    assert str(err.value) == "Ship overlaps a previously placed ship"
                    game = game_cache

    """
    Vertical obstacle, horizontal ship placement
    """
    game_list = []
    placement_list = []
    game_rows = 10
    game_cols = 10
    obs_orient = "vertical"
    for obs_length in range(2, 6):
        for obs_col in range(1, 11):
            for obs_row in range(1, game_rows - obs_length):
                game = Game(game_rows, game_cols)
                game.place_ship(obs_length, obs_orient, obs_row, obs_col)
                game_list.append(game)
                placement_list.append({"len": obs_length, "ori": obs_orient, "row": obs_row, "col": obs_col})

    ship_orient = "horizontal"
    for game, obstacle in zip(game_list, placement_list):
        game_cache = copy.copy(game)
        for ship_length in range(2, 6):
            for ship_row in range(min(obstacle["col"], game_rows - ship_length + 1), max(obstacle["col"] - ship_length + 1, 1)):
                for ship_col in range(obstacle["row"] + obstacle["len"], obstacle["col"]):
                    with pytest.raises(Exception) as err:
                        game.place_ship(ship_length, ship_orient, ship_row, ship_col)
                    assert str(err.value) == "Ship overlaps a previously placed ship"
                    game = game_cache

#@pytest.mark.skip(reason="")
def test_game_ship_placement_moves_unplaced_to_placed():
    game = Game()
    game.place_ship(2, "horizontal", 1, 1)
    assert len(game.ships_unplaced) < 5
    assert len(game.ships_placed) > 0

#@pytest.mark.skip(reason="")
def test_game_make_shot_adds_to_shots_made_or_raises_exception():
    game = Game()
    shots_made = []
    for row in range(1, game.rows + 1):
        for col in range(1, game.cols + 1):
            game.make_shot(row, col)
            shots_made.append((row, col))
            assert game.shots_made == shots_made
    for row in [-1, 0, 11, 12]:
        for col in [-1, 0, 11, 12]:
            with pytest.raises(Exception) as err:
                game.make_shot(row, col)
            assert str(err.value) == "Oops! That shot missed the board!"

#@pytest.mark.skip(reason="")
def test_generate_opponent_board_produces_ship_placements():
    game = Game()
    io = TerminalInterfaceHelperMock()
    ui = UserInterface(io, game)
    ui.generate_opponent_board()
    assert str(ui.opponent_game.ship_placements) == "".join([
        '[ShipPlacement(length=2, orientation=horizontal, row=2, col=2), ',
        'ShipPlacement(length=3, orientation=horizontal, row=3, col=3), ',
        'ShipPlacement(length=3, orientation=vertical, row=4, col=6), '
        'ShipPlacement(length=4, orientation=horizontal, row=8, col=2), '
        'ShipPlacement(length=5, orientation=vertical, row=1, col=10)]'
    ])

#@pytest.mark.skip(reason="")
def test_import_shots_adds_shot_positions_to_shots_received():
    player_game = Game()
    opponent_game = Game()
    shots_received = []
    for row in range(2,11,2):
        for col in range(1,10,2):
            opponent_game.make_shot(row, col)
            shots_received.append((row, col))
    player_game.import_shots(opponent_game)
    assert player_game.shots_received == shots_received

#@pytest.mark.skip(reason="")
def test_ships_placed_dict_shows_position_after_ship_placement():
    game = Game()
    game.place_ship(2, "horizontal", 1, 1)
    game.place_ship(5, "vertical", 6, 10)
    assert game.ships_placed == {
        2: {"position": [(1, 1), (1, 2)], "hits": [], "sunk": False},
        5: {"position": [(6, 10), (7, 10), (8, 10), (9, 10), (10, 10)], 
            "hits": [], "sunk": False}
        }
   
#@pytest.mark.skip(reason="") 
def test_ships_placed_dict_shows_hits_after_importing_shots():
    game = Game()
    game.place_ship(2, "horizontal", 1, 1)
    game.place_ship(5, "vertical", 6, 10)
    shot_range = zip([1, 1, 6, 8, 10, 5, 3, 1, 2, 4], [1, 2, 10, 10, 10, 6, 10, 8, 7, 9])
    for shot_row, shot_col in shot_range:
        game.make_shot(shot_row, shot_col)
        print((shot_row, shot_col))
    game.import_shots(game)
    assert game.ships_placed == {
        2: {"position": [(1, 1), (1, 2)], "hits": [(1, 1), (1, 2)], "sunk": True},
        5: {"position": [(6, 10), (7, 10), (8, 10), (9, 10), (10, 10)], 
            "hits": [(6, 10), (8, 10), (10, 10)], "sunk": False}
        }

#@pytest.mark.skip(reason="")
def test_game_state_changes_when_player_ships_all_sunk():
    player_game = Game()
    ship_place_zip = zip([2, 3, 3, 4, 5],
                         ["horizontal", "vertical", "horizontal", "vertical", "horizontal"], 
                         [1, 2, 4, 6, 10], 
                         [1, 2, 5, 5, 6])
    shots_zip = zip([1, 1, 2, 3, 4, 4, 4, 4, 6, 7, 8, 9, 10, 10, 10, 10, 10],
                     [1, 2, 2, 2, 2, 5, 6, 7, 5, 5, 5, 5, 6, 7, 8, 9, 10])
    for ship_place in ship_place_zip:
        player_game.place_ship(ship_place[0], ship_place[1], ship_place[2], ship_place[3])
    
    opponent_game = copy.copy(player_game)
    for shot in shots_zip:
        opponent_game.make_shot(shot[0], shot[1])
    
    player_game.import_shots(opponent_game)
    assert player_game.game_state == "lost"


class TestUserInterface(unittest.TestCase):

    #@pytest.mark.skip(reason="")
    def test_ships_constrained_to_board_in_interface(self):
        ship_choices = [str(ship) for ship in list(range(2,6))]
        orient_choices = ["h", "v"]
        
        for ship_choice in ship_choices:
            game = Game(ships=[Ship(int(ship_choice))])
            for orient_choice in orient_choices:
                first_row_choices = [str(row) for row in list(range(1, 11))]
                first_col_choices = [str(col) for col in [0] + list(range(12 - int(ship_choice), 11))]
                second_col_choices = [str(col) for col in list(range(1, 11 - int(ship_choice)))]
                for row_choice in first_row_choices:
                    for col_choice in first_col_choices:
                        for col_choice_2 in second_col_choices:
                            row_choice_2 = row_choice

                            game_board_builder = Game()
                            if orient_choice == "h":
                                build_row, build_col, build_orient = int(row_choice_2), int(col_choice_2), "horizontal"
                            else:
                                build_col, build_row, build_orient = int(row_choice_2), int(col_choice_2), "vertical"
                            game_board_builder.place_ship(int(ship_choice), build_orient, build_row, build_col)

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
                            game = Game(ships=[Ship(int(ship_choice))])

                            io = TerminalInterfaceHelperMock()
                            interface = UserInterface(io, game)
                            io.expect_print("Welcome to the game!")
                            io.expect_print("Set up your ships first.")
                            io.expect_print("You have these ships remaining: " + ship_choice)
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
                            interface.run()

    #@pytest.mark.skip(reason="")
    def test_interface_asks_for_ship_placements_until_all_placed(self):
        game = Game()
        io = TerminalInterfaceHelperMock()
        interface = UserInterface(io, game)
        
        ship_choice = [3,5,4,3,2]
        orient_choice = ["v", "h", "v", "v", "h",]
        row_choice = [1, 1, 4, 8, 7]
        col_choice = [1, 2, 6, 8, 3]
        ships_remaining = ["2, 3, 3, 4, 5", "2, 3, 4, 5", "2, 3, 4", "2, 3", "2"]

        previous_board_state = [
                                [".",".",".",".",".",".",".",".",".","."],
                                [".",".",".",".",".",".",".",".",".","."],
                                [".",".",".",".",".",".",".",".",".","."],
                                [".",".",".",".",".",".",".",".",".","."],
                                [".",".",".",".",".",".",".",".",".","."],
                                [".",".",".",".",".",".",".",".",".","."],
                                [".",".",".",".",".",".",".",".",".","."],
                                [".",".",".",".",".",".",".",".",".","."],
                                [".",".",".",".",".",".",".",".",".","."],
                                [".",".",".",".",".",".",".",".",".","."]
                                ]
        expected_board_state = []

        for i in range(len(ship_choice)):
            for r in range(len(previous_board_state)):
                for c in range(len(previous_board_state[r])):
                    if orient_choice[i] == "h" \
                        and r + 1 == row_choice[i] \
                            and c + 1 >= col_choice[i] \
                                and c + 2 <= col_choice[i] + ship_choice[i]:
                        previous_board_state[r][c] = "S"
                        ## debug
                        # rows = []
                        # for row in previous_board_state:
                        #     rows.append("".join(row))
                        # print("\n".join(rows), "\n")

                    elif orient_choice[i] == "v" \
                        and c + 1 == col_choice[i] \
                            and r + 1 >= row_choice[i] \
                                and r + 2 <= row_choice[i] + ship_choice[i]:
                        ## debug
                        # print(f"r: {r}, row+length: {row_choice[i] + ship_choice[i]}")
                        # print(f"r: {r}, c: {c}, prev[r][c]: {previous_board_state[r][c]}")

                        previous_board_state[r][c] = "S"
                        
                        ## debug
                        # print(previous_board_state)
                        # rows = []
                        # for row in previous_board_state:
                        #     print(row)
                        #     rows.append("".join(row))
                        # print("\n".join(rows), "\n")
                                
            expected_board_state.append(copy.deepcopy(previous_board_state))
        for board in range(len(expected_board_state)):
            rows = []
            for row in expected_board_state[board]:
                rows.append("".join(row))
            expected_board_state[board] = "\n".join(rows)

        for board in expected_board_state:
            print(board)

        io.expect_print("Welcome to the game!")
        io.expect_print("Set up your ships first.")
        for i in range(len(ship_choice)):
            io.expect_print("You have these ships remaining: " + \
                            ships_remaining[i])
            io.expect_print("Which do you wish to place?")
            io.provide(str(ship_choice[i]))
            io.expect_print("Vertical or horizontal? [vh]")
            io.provide(orient_choice[i])
            io.expect_print("Which row?")
            io.provide(str(row_choice[i]))
            io.expect_print("Which column?")
            io.provide(str(col_choice[i]))
            io.expect_print("OK.")
            io.expect_print("This is your board now:")
            io.expect_print(expected_board_state[i])
        
        interface.run()