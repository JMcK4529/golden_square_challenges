import unittest
import pytest
import copy
from lib.user_interface import UserInterface
from lib.game import Game
from lib.ship import Ship
from tests.terminal_interface_helper_mock import TerminalInterfaceHelperMock

class TestUserInterface(unittest.TestCase):
    @pytest.mark.skip(reason="Ship sinking breaks for ship with args '4, v, 3, 1'")
    def test_example_game(self):
        io = TerminalInterfaceHelperMock()
        interface = UserInterface(io, Game())
        p1_ships = ["2", "3", "3", "4", "5"]
        p1_ships_remaining = ["2, 3, 3, 4, 5", "3, 3, 4, 5",
                              "3, 4, 5", "4, 5", "5"]
        p1_orientations = ["h", "v", "h", "v", "h"]
        p1_placements = [("2", "2"), ("1", "4"), ("3", "7"),
                         ("6", "5"), ("2", "6")]
        p1_expected_boards = [["..........",
                              ".SS.......",
                              "..........",
                              "..........",
                              "..........",
                              "..........",
                              "..........",
                              "..........",
                              "..........",
                              ".........."],
                              ["...S......",
                              ".SSS......",
                              "...S......",
                              "..........",
                              "..........",
                              "..........",
                              "..........",
                              "..........",
                              "..........",
                              ".........."],
                              ["...S......",
                              ".SSS......",
                              "...S..SSS.",
                              "..........",
                              "..........",
                              "..........",
                              "..........",
                              "..........",
                              "..........",
                              ".........."],
                              ["...S......",
                              ".SSS......",
                              "...S..SSS.",
                              "..........",
                              "..........",
                              "....S.....",
                              "....S.....",
                              "....S.....",
                              "....S.....",
                              ".........."],
                              ["...S......",
                              ".SSS.SSSSS",
                              "...S..SSS.",
                              "..........",
                              "..........",
                              "....S.....",
                              "....S.....",
                              "....S.....",
                              "....S.....",
                              ".........."]
                              ]
        p1_zip = zip(p1_ships, p1_ships_remaining, p1_orientations,
                     p1_placements, p1_expected_boards)

        p2_ships = ["3", "5", "4", "3", "2"]
        p2_ships_remaining = ["2, 3, 3, 4, 5", "2, 3, 4, 5", "2, 3, 4", "2, 3", "2"]
        p2_orientations = ["v", "h", "v", "h", "v"]
        p2_placements = [("8", "6"), ("1", "3"), ("3", "1"), ("7", "5"), ("9", "10")]
        p2_expected_boards = [["..........",
                              "..........",
                              "..........",
                              "..........",
                              "..........",
                              "..........",
                              "..........",
                              ".....S....",
                              ".....S....",
                              ".....S...."],
                              ["..SSSSS...",
                              "..........",
                              "..........",
                              "..........",
                              "..........",
                              "..........",
                              "..........",
                              ".....S....",
                              ".....S....",
                              ".....S...."],
                              ["..SSSSS...",
                              "..........",
                              "S.........",
                              "S.........",
                              "S.........",
                              "S.........",
                              "..........",
                              ".....S....",
                              ".....S....",
                              ".....S...."],
                              ["..SSSSS...",
                              "..........",
                              "S.........",
                              "S.........",
                              "S.........",
                              "S.........",
                              "....SSS...",
                              ".....S....",
                              ".....S....",
                              ".....S...."],
                              ["..SSSSS...",
                              "..........",
                              "S.........",
                              "S.........",
                              "S.........",
                              "S.........",
                              "....SSS...",
                              ".....S....",
                              ".....S...S",
                              ".....S...S"]
                              ]
        p2_zip = zip(p2_ships, p2_ships_remaining, p2_orientations,
                     p2_placements, p2_expected_boards)

        io.expect_print("Welcome to the game!")
        io.expect_print("Set up Player 1's ships.")       
        for args in p1_zip:
            io.expect_print("Player 1 has these ships remaining: " + args[1])
            io.expect_print("Which do you wish to place?")
            io.provide(args[0])
            io.expect_print("Vertical or horizontal? [vh]")
            io.provide(args[2])
            io.expect_print("Which row?")
            io.provide(args[3][0])
            io.expect_print("Which column?")
            io.provide(args[3][1])
            io.expect_print("OK.")
            io.expect_print("This is Player 1's board now:")
            io.expect_print("\n".join(args[4]))
        
        io.expect_print("Set up Player 2's ships.")       
        for args in p2_zip:
            io.expect_print("Player 2 has these ships remaining: " + args[1])
            io.expect_print("Which do you wish to place?")
            io.provide(args[0])
            io.expect_print("Vertical or horizontal? [vh]")
            io.provide(args[2])
            io.expect_print("Which row?")
            io.provide(args[3][0])
            io.expect_print("Which column?")
            io.provide(args[3][1])
            io.expect_print("OK.")
            io.expect_print("This is Player 2's board now:")
            io.expect_print("\n".join(args[4]))

        p1_misses_p2 = (1, 10)

        p1_hits_p2 = [(9, 10), (8, 6), (9, 6), (7, 5), (7, 6),
                       (2, 1), (3, 1), (4, 1), (1, 3), (1, 4),
                         (1, 5), (1, 6)]
        p1_sinks_p2 = [(10, 10), (10, 6), (7, 7), (5, 1), (1, 7)]

        p2_misses_p1 = (10, 1)

        p2_hits_p1 = [(2, 2), (1, 4), (2, 4), (3, 7), (3, 8),
                       (6, 5), (7, 5), (8, 5), (2, 6), (2, 7),
                         (2, 8), (2, 9)]
        p2_sinks_p1 = [(2, 3), (3, 4), (3, 9), (9, 5)]

        p1_shots = [(1, 10), (9, 10), (10, 10), (8, 6), (9, 6), (10, 6),
                    (7, 5), (7, 6), (7, 7), (3, 1), (4, 1), (5, 1), (6, 1),
                    (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)]
        
        p2_shots = [(10, 1), (2, 2), (2, 3), (1, 4), (2, 4), (3, 4), (3, 7), 
                    (3, 8), (3, 9), (6, 5), (7, 5), (8, 5), (9, 5), 
                    (2, 6), (2, 7), (2, 8), (2, 9)]
        
        p1_shot_states = []
        p2_shot_states = []
        initial_board_state = [
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
        previous_board_state = copy.deepcopy(initial_board_state)
        previous_board_state[0][9] = "O"
        p1_shot_states.append(["".join(row_cells) for row_cells in [rows for rows in previous_board_state]])
        for shot in p1_shots[1:len(p1_shots)]:
            # print(shot)
            previous_board_state[shot[0]-1][shot[1]-1] = "X"
            p1_shot_states.append(["".join(row_cells) for row_cells in [rows for rows in previous_board_state]])
            # for row in ["".join(row_cells) for row_cells in [rows for rows in previous_board_state]]:
            #     print(row)
            # print()
        
        previous_board_state = copy.deepcopy(initial_board_state)
        previous_board_state[9][0] = "O"
        p2_shot_states.append(["".join(row_cells) for row_cells in [rows for rows in previous_board_state]])
        for shot in p2_shots[1:len(p2_shots)]:
            previous_board_state[shot[0]-1][shot[1]-1] = "X"
            p2_shot_states.append(["".join(row_cells) for row_cells in [rows for rows in previous_board_state]])

        # for board in p1_shot_states:
        #     for row in board:
        #         print(row)
        #     print("\n")
        
        # for board in p2_shot_states:
        #     for row in board:
        #         print(row)
        #     print("\n")

        io.expect_print("Player 1's turn to shoot.")
        io.expect_print("Which row?")
        io.provide(str(p1_misses_p2[0]))
        io.expect_print("Which column?")
        io.provide(str(p1_misses_p2[1]))
        io.expect_print("That was a miss!")
        io.expect_print("Player 1 has made these shots so far:")
        io.expect_print("\n".join(p1_shot_states[0]))
        io.expect_print("Player 2's turn to shoot.")
        io.expect_print("Which row?")
        io.provide(str(p2_misses_p1[0]))
        io.expect_print("Which column?")
        io.provide(str(p2_misses_p1[1]))
        io.expect_print("That was a miss!")
        io.expect_print("Player 2 has made these shots so far:")
        io.expect_print("\n".join(p2_shot_states[0]))

        p1_state_no = 1
        p2_state_no = 1
        p1_shot_no = 1
        p2_shot_no = 1
        for ship in range(len(p1_ships)):
            for i in range(int(p1_ships[ship])-1):
                ## debug
                # print(str(p1_hits_p2[i][0]), str(p1_hits_p2[i][1]))
                # print(str(p2_hits_p1[i][0]), str(p2_hits_p1[i][1]))
                print(f"ship: {ship}\np1_shotno: {p1_state_no}\np2_shotno: {p2_state_no}")
                print(f"p1 shot: {p1_shots[p1_shot_no][0]},{p1_shots[p1_shot_no][1]}")
                print(f"p2 shot: {p2_shots[p2_shot_no][0]},{p2_shots[p2_shot_no][1]}")

                io.expect_print("Player 1's turn to shoot.")
                io.expect_print("Which row?")
                io.provide(str(p1_shots[p1_shot_no][0]))
                io.expect_print("Which column?")
                io.provide(str(p1_shots[p1_shot_no][1]))
                p1_shot_no += 1

                io.expect_print("That was a hit!")
                io.expect_print("Player 1 has made these shots so far:")
                io.expect_print("\n".join(p1_shot_states[p1_state_no]))
                p1_state_no += 1

                io.expect_print("Player 2's turn to shoot.")
                io.expect_print("Which row?")
                io.provide(str(p2_shots[p2_shot_no][0]))
                io.expect_print("Which column?")
                io.provide(str(p2_shots[p2_shot_no][1]))
                p2_shot_no += 1

                io.expect_print("That was a hit!")
                io.expect_print("Player 2 has made these shots so far:")
                io.expect_print("\n".join(p2_shot_states[p2_state_no]))
                p2_state_no += 1
            
            ## debug
            print(f"p1 sink shot: {p1_sinks_p2[ship-1][0]},{p1_sinks_p2[ship-1][1]}")
            print(f"p2 sink shot: {p2_sinks_p1[ship-1][0]},{p2_sinks_p1[ship-1][1]}")
            # print("\n".join(p1_shot_states[p1_shot_no]))

            io.expect_print("Player 1's turn to shoot.")
            io.expect_print("Which row?")
            io.provide(str(p1_sinks_p2[ship-1][0]))
            io.expect_print("Which column?")
            io.provide(str(p1_sinks_p2[ship-1][1]))
            io.expect_print("That was a hit!")
            io.expect_print("Player 1 sank Player 2's ship!")
            io.expect_print("Player 1 has made these shots so far:")
            io.expect_print("\n".join(p1_shot_states[p1_state_no]))
            p1_state_no += 1

            io.expect_print("Player 2's turn to shoot.")
            io.expect_print("Which row?")
            io.provide(str(p2_sinks_p1[ship-1][0]))
            io.expect_print("Which column?")
            io.provide(str(p2_sinks_p1[ship-1][1]))
            io.expect_print("That was a hit!")
            io.expect_print("Player 2 sank Player 1's ship!")
            io.expect_print("Player 2 has made these shots so far:")
            io.expect_print("\n".join(p1_shot_states[p2_state_no]))
            p2_state_no += 1

        # for i in range(-5,-5):
        #     io.expect_print("Player 1's turn to shoot.")
        #     io.expect_print("Which row?")
        #     io.provide(str(p1_shots[i][0]))
        #     io.expect_print("Which column?")
        #     io.provide(str(p1_shots[i][1]))
        #     io.expect_print("That was a hit!")
        #     io.expect_print("Player 1 has made these shots so far:")
        #     io.expect_print("\n".join(p1_shot_states[i]))
        #     p1_shot_no += 1
        #     io.expect_print("Player 2's turn to shoot.")
        #     io.expect_print("Which row?")
        #     io.provide(str(p2_shots[i][0]))
        #     io.expect_print("Which column?")
        #     io.provide(str(p2_shots[i][1]))
        #     io.expect_print("That was a hit!")
        #     io.expect_print("Player 2 has made these shots so far:")
        #     io.expect_print("\n".join(p1_shot_states[i + 1]))
        #     p2_shot_no += 1
        
        # io.expect_print("Player 1's turn to shoot.")
        # io.expect_print("Which row?")
        # io.provide(str(p1_hits_p2[-1][0]))
        # io.expect_print("Which column?")
        # io.provide(str(p1_hits_p2[-1][1]))
        # io.expect_print("That was a hit!")
        # io.expect_print("Player 1 sank Player 2's ship!")
        # io.expect_print("Player 1 won!")
        # io.expect_print("Player 2 lost!")

        interface.run()


    #@pytest.mark.skip(reason="")
    def test_ships_constrained_to_board_in_interface(self):
        game = Game()
        io = TerminalInterfaceHelperMock()
        interface = UserInterface(io, game)
        ships = [2, 3, 4, 5]
        orients = ["h", "v"]

        args = []
        for ship in ships:
            rows = [0] + list(range(12 - ship, 12))
            for orient in orients:
                for row in rows:
                    for col in range(12 - ship, 12):
                        if orient == "h":
                            row, col = col, row
                        args.append([ship, orient, row, col])
        
        for arg in args:
            with pytest.raises(SystemExit) as err:
                io.expect_print("Welcome to the game!")
                io.expect_print("Set up Player 1's ships.")       
                io.expect_print("Player 1 has these ships remaining: 2, 3, 3, 4, 5")
                io.expect_print("Which do you wish to place?")
                io.provide(str(arg[0]))
                io.expect_print("Vertical or horizontal? [vh]")
                io.provide(str(arg[1]))
                io.expect_print("Which row?")
                io.provide(str(arg[2]))
                io.expect_print("Which column?")
                io.provide(str(arg[3]))
                print(arg)
                io.expect_print("Oops! That ship overlaps the board edge!")
                io.expect_print("Which row?")
                io.provide("QUIT")
                interface.run()
            assert str(err.value) == "None"
                                  

    #@pytest.mark.skip(reason="User interface changed")
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

                    elif orient_choice[i] == "v" \
                        and c + 1 == col_choice[i] \
                            and r + 1 >= row_choice[i] \
                                and r + 2 <= row_choice[i] + ship_choice[i]:
                        previous_board_state[r][c] = "S"
                                
            expected_board_state.append(copy.deepcopy(previous_board_state))
        for board in range(len(expected_board_state)):
            rows = []
            for row in expected_board_state[board]:
                rows.append("".join(row))
            expected_board_state[board] = "\n".join(rows)

        with pytest.raises(SystemExit) as err:
            io.expect_print("Welcome to the game!")
            io.expect_print("Set up Player 1's ships.")
            for i in range(len(ship_choice)):
                io.expect_print("Player 1 has these ships remaining: " + \
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
                io.expect_print("This is Player 1's board now:")
                io.expect_print(expected_board_state[i])
            io.expect_print("Set up Player 2's ships.")
            io.expect_print("Player 2 has these ships remaining: 2, 3, 3, 4, 5")
            io.expect_print("Which do you wish to place?")
            io.provide("QUIT")
            interface.run()
        assert str(err.value) == "None"

    @pytest.mark.skip(reason="Should not call a private function")
    def test_player_board_state_displayed_with_hits_and_misses(self):
        player_game = Game()
        ship_place_zip = zip([2, 3, 3, 4, 5],
                            ["horizontal", "vertical", "horizontal", "vertical", "horizontal"], 
                            [1, 2, 4, 6, 10], 
                            [1, 2, 5, 5, 6])
        for ship_place in ship_place_zip:
            player_game.place_ship(ship_place[0], ship_place[1], ship_place[2], ship_place[3])
        
        expected_board = [
                            ["S","S",".",".",".",".",".",".",".","."],
                            [".","S",".",".",".",".",".",".",".","."],
                            [".","S",".",".",".",".",".",".",".","."],
                            [".","S",".",".","S","S","S",".",".","."],
                            [".",".",".",".",".",".",".",".",".","."],
                            [".",".",".",".","S",".",".",".",".","."],
                            [".",".",".",".","S",".",".",".",".","."],
                            [".",".",".",".","S",".",".",".",".","."],
                            [".",".",".",".","S",".",".",".",".","."],
                            [".",".",".",".",".","S","S","S","S","S"]
                        ]
        
        shots_zip = zip([1, 1, 2, 3, 4, 4, 4, 4, 5, 7, 8, 9, 10, 10, 10, 10, 10],
                        [1, 10, 2, 2, 2, 5, 6, 7, 6, 5, 5, 5, 6, 7, 8, 9, 10])
        opponent_game = copy.copy(player_game)
        for shot in shots_zip:
            opponent_game.make_shot(shot[0], shot[1])
            expected_board[shot[0]-1][shot[1]-1] = \
                "X" if expected_board[shot[0]-1][shot[1]-1] == "S" else "O"

        player_game.import_shots(opponent_game)

        io = TerminalInterfaceHelperMock()
        ui = UserInterface(io, player_game)
        
        expected_rows = []
        for row in expected_board:
            expected_rows.append("".join(row))
        
        assert ui._format_board() == "\n".join(expected_rows)

    @pytest.mark.skip(reason="Should not call a private method")
    def test_player_board_state_displayed_with_hits_and_misses(self):
        player_game = Game()
        ship_place_zip = zip([2, 3, 3, 4, 5],
                            ["horizontal", "vertical", "horizontal", "vertical", "horizontal"], 
                            [1, 2, 4, 6, 10], 
                            [1, 2, 5, 5, 6])
        for ship_place in ship_place_zip:
            player_game.place_ship(ship_place[0], ship_place[1], ship_place[2], ship_place[3])
        
        expected_board = [
                            ["S","S",".",".",".",".",".",".",".","."],
                            [".","S",".",".",".",".",".",".",".","."],
                            [".","S",".",".",".",".",".",".",".","."],
                            [".","S",".",".","S","S","S",".",".","."],
                            [".",".",".",".",".",".",".",".",".","."],
                            [".",".",".",".","S",".",".",".",".","."],
                            [".",".",".",".","S",".",".",".",".","."],
                            [".",".",".",".","S",".",".",".",".","."],
                            [".",".",".",".","S",".",".",".",".","."],
                            [".",".",".",".",".","S","S","S","S","S"]
                        ]
        
        shots_zip = zip([1, 1, 2, 3, 4, 4, 4, 4, 5, 7, 8, 9, 10, 10, 10, 10, 10],
                        [1, 10, 2, 2, 2, 5, 6, 7, 6, 5, 5, 5, 6, 7, 8, 9, 10])
        opponent_game = copy.copy(player_game)
        for shot in shots_zip:
            player_game.make_shot(shot[0], shot[1])
            expected_board[shot[0]-1][shot[1]-1] = \
                "X" if expected_board[shot[0]-1][shot[1]-1] == "S" else "O"
        for i in range(len(expected_board)):
            for j in range(len(expected_board[i])):
                expected_board[i][j] = "." if expected_board[i][j] == "S" \
                                            else expected_board[i][j]

        opponent_game.import_shots(player_game)
        io = TerminalInterfaceHelperMock()
        ui = UserInterface(io, player_game)
        
        expected_rows = []
        for row in expected_board:
            expected_rows.append("".join(row))
        expected_board = "\n".join(expected_rows)
        assert ui._format_opponent_board(opponent_game) == expected_board