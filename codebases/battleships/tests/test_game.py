import copy
import pytest
from lib.game import Game

"""
Initialises with a length and width of 10
"""
def test_initialises_with_a_length_and_width_of_10():
    game = Game()
    assert game.rows == 10
    assert game.cols == 10

"""
Initialises with five ships of length 2, 3, 3, 4, 5
"""
def test_initialises_with_five_ships_of_right_length():
    game = Game()
    unplaced_ships = game.unplaced_ships()
    assert len(unplaced_ships) == 5
    assert unplaced_ships[0].length == 2
    assert unplaced_ships[1].length == 3
    assert unplaced_ships[2].length == 3
    assert unplaced_ships[3].length == 4
    assert unplaced_ships[4].length == 5

"""
Initialises with a totally empty board
"""
def test_initialises_with_a_totally_empty_board():
    game = Game()
    for row in range(1, 11):
        for col in range(1, 11):
            assert not game.ship_at(row, col)

"""
When we place a ship
Then its place on the board is marked out
"""
def test_when_we_place_a_ship_then_its_place_on_the_board_is_marked_out():
    game = Game()
    game.place_ship(length=2, orientation="vertical", row=3, col=2)
    assert game.ship_at(3, 2)
    assert game.ship_at(4, 2)
    assert not game.ship_at(3, 3)
    assert not game.ship_at(4, 3)
    assert not game.ship_at(3, 1)
    assert not game.ship_at(4, 1)

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
                    assert str(err.value) == "Oops! That ship overlaps the board edge!"
                
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
                # print(game.ships_unplaced, "\n", (obs_length, obs_orient, obs_row, obs_col))
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
                    assert str(err.value) == "Oops! That ship overlaps a previously placed ship!"
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
                    assert str(err.value) == "Oops! That ship overlaps a previously placed ship!"
                    game = game_cache

def test_game_ship_placement_moves_unplaced_to_placed():
    game = Game()
    game.place_ship(2, "horizontal", 1, 1)
    assert len(game.ships_unplaced) < 5
    assert len(game.ships_placed) > 0

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

def test_ships_placed_dict_shows_position_after_ship_placement():
    game = Game()
    game.place_ship(2, "horizontal", 1, 1)
    game.place_ship(5, "vertical", 6, 10)
    assert game.ships_placed == {
        "ship0": {"length": 2, "position": [(1, 1), (1, 2)], 
                  "hits": [], "sunk": False
                  },
        "ship1": {"length": 5, 
                  "position": [(6, 10), (7, 10), (8, 10), (9, 10), (10, 10)], 
                  "hits": [], "sunk": False
                  }
        }
   
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
        "ship0": {"length": 2,
                  "position": [(1, 1), (1, 2)],
                  "hits": [(1, 1), (1, 2)], "sunk": True
                  },
        "ship1": {"length": 5,
                  "position": [(6, 10), (7, 10), (8, 10), (9, 10), (10, 10)],
                  "hits": [(6, 10), (8, 10), (10, 10)], "sunk": False
                  }
        }

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

def test_game_state_changes_when_opponent_ships_all_sunk():
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
        player_game.make_shot(shot[0], shot[1])

    opponent_game.import_shots(player_game)
    player_game.check_win(opponent_game)
    assert player_game.game_state == "won"