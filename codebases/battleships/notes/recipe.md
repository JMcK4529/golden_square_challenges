# Notes

## Current State of Program

### run.py
- Defines a class TerminalIO which reads and prints outputs in terminal
    - readline() reads lines via stdin
    - write() writes lines via stdout
- Instantiates TerminalIO
- Instantiates Game
- Instantiates UserInterface
- Calls UserInterface.run method

### user_interface.;py
- Defines a class UserInterface which handles communication with the user
    - \_\_init\_\_() creates self.io and self.game, which store a TerminalIO and Game instance, respectively
    - run() writes instructions to the terminal, including:
        - A formatted string containing the results of a call to self._ships_unplaced_message()
        - A call to self._prompt_for_ship_placement()
        - A call to self._show(self._format_board())
    - \_show(message) uses TerminalIO to write message + "\\n" to the terminal
    - \_prompt(message) uses TerminalIO to write message + "\\n" to the terminal and to return a stripped readline()
    - \_ships_unplaced_message() returns a string containing the lengths of all ships in Game.unplaced_ships()
    - \_prompt_for_ship_placement() uses a series of calls to self._prompt(message) to get parameters (length, orientation, row, col) to pass to Game.place_ship(length, orientation, row, col)
    - \_format_board() creates Game.rows lists of cells ["."] (of length Game.cols), joining these cells with "" and joining the rows with "\\n" -> in future calls, Game.ship_at(row, col) is used to change the cell to ["S"] if Game.ship_at(row, col) == True

### game.py
- Defines a class Game which handles game rules (currently relating to the placement of ships)
    - \_\_init\_\_(rows=10, cols=10) instantiates the class with three public variables:
        - self.ships_placed = [] -> later containing instances of the ShipPlacement class
        - self.rows = rows -> default = 10
        - self.cols = cols -> default = 10
    - unplaced_ships() returns a list of 5 instances of the Ship class, with varying Ship.length variables
    - place_ship(length, orientation, row, col) creates an instance of ShipPlacement, passing it the length, orientation, row and col arguments, then appends it to self.ships_placed
    - ship_at(row, col) uses the ShipPlacement.covers(row, col) method to return a Boolean which is True if part of the ship covers the cell at row, col; else False

### ship_placement.py
- Defines a class ShipPlacement which handles logic concerning which cells/rows/cols are covered by a ship
    - \_\_init\_\_(length, orientation, row, col) instantiates the class with four public variables:
        - self.length = length -> The length of the ship
        - self.orientation = orientation -> "horizontal" (up to down) or "vertical" (left to right)
        - self.row = row -> The row that ship starts from
        - self.col = col -> The column that ship starts from
    - covers(row, col) returns:
        - True if the ship is horizontal and self.col + self.length >= col
        - True if ship is vertical and self.row + self.length >= row
        - False otherwise
    - \_\_repr\_\_() sets the representation of the class (when printed) to be a formatted string:
        - f"ShipPlacement(length={self.length}, orientation={self.orientation}, row={self.row}, col={self.col})"
        - e.g. "ShipPlacement(length=3, orientation=horizontal, row=2, col=4)"

### ship.py
- Defines a class Ship (using dataclass) which stores a public variable (length) which is passed to the constructor (e.g. Ship(3).length == 3)

## What Next?

### User Stories

```
As a player
So that I can prepare for the game
I would like to place a ship in a board location
```
Implemented for a single ship.

```
As a player
So that I can play a more interesting game
I would like to have a range of ship sizes to choose from
```
Ship choices already implemented.
Single ship placement already implemented.
Multiple ship placement not yet implemented in Game or UserInterface.

```
As a player
So the game is more fun to play
I would like a nice command line interface that lets me enter ship positions and
shots using commands.
```
Interface already implemented.
Single ship placement already implemented.
Multiple ship placement not yet implemented in Game or UserInterface.
Shot functionality not yet implemented in Game or UserInterface.

```
As a player
So that I can create a layout of ships to outwit my opponent
I would like to be able to choose the directions my ships face in
```
Already implemented.

```
As a player
So that I can have a coherent game
I would like ships to be constrained to be on the board
```
~~Not yet implemented.~~
~~Implemented in Game.place_ship method, not yet handled in UserInterface.~~
Implemented in Game.place_ship method and exception handling implemented in UserInterface.

```
As a player
So that I can have a coherent game
I would like ships to be constrained not to overlap
```
~~Not yet implemented.~~
~~Implemented in Game.place_ship method, not yet handled in UserInterface.~~
Implemented in Game.place_ship method and handled in UserInterface.

```
As a player
So that I can win the game
I would like to be able to fire at my opponent's board
```
Not yet implemented.

```
As a player
So that I can refine my strategy
I would like to know when I have sunk an opponent's ship
```
Not yet implemented.

```
As a player
So that I know when to finish playing
I would like to know when I have won or lost
```
Not yet implemented.

```
As a player
So that I can consider my next shot
I would like to be able to see my hits and misses so far
```
Not yet implemented.

```
As a player
So that I can play against a human opponent
I would like to play a two-player game
```
Not yet implemented.

### Next Steps

#### Constrain ships to the board.
- If a ShipPlacement has parameters which would place the ship over the edge of the board, prevent this behaviour and ask for a different input.
- Cannot choose row < 0, col < 0
- Cannot choose row > Game.rows, col > Game.cols
- When orientation "horizontal":
    - Cannot choose col > Game.cols - length
- When orientation "vertical":
    - Cannot choose row > Game.rows - length
- Asking for a different input when an illegal ship placement is declared means changing Game.place_ship method so it validates inputs, and using a try/except in UserInterface._prompt_for_ship_placement method so that it only proceeds once a valid input is taken
- Write a test that uses lots of game board sizes, ship sizes and ship placements, making sure that whenever either end of the ship is < 0 or > Game.cols or > Game.rows we raise an Exception

> This is now passing tests for the first ship placement.  
> [TODO]: Will have to expand test when additional ships can be placed. Expect passes because UserInterface._prompt_for_ship_placement has been changed, and this same method can be called to get future ship positions.

#### Disallow ship overlaps.
- We can achieve this with argument validation in Game.place_ship method (similar to above)
- Call the first placed ship "obstacle". Call the second ship "ship".
- Write a test that uses lots of obstacle sizes and placements (and both orientations), then test that an exception is raised whenever the ship is placed in a way that would make it overlap the obstacle at any point

> This passes the test using Game.place_ship
> [TODO]: Test in the user interface
> [TODO]: Test with multiple ships

#### Add multiple ships to the board.
- We start with 5 ships of different lengths, and should be able to place them all on the board.
- We should keep asking the user to choose a ship and place it until there are no ships left to place
- We can implement the asking with a while loop and expansion of UserInterface.run method
- Write a test that uses the terminal_interface_helper_mock to check that ship placements are requested until all ships have been placed

> Test written and passed!

#### Declare shots.
- Add a method to Game & UserInterface to allow the player to start making shots.
- Should be able to declare row and col
- Should store all shots made in a variable in Game
- Write a test that checks for functionality like this:
```python
game = Game()
game.make_shot(1, 1) # => returns nothing but adds (1,1) to game.shots_made
game.shots_made # => [(1, 1)]
game.make_shot(6,8)
game.shots_made # => [(1, 1), (6, 8)]
```

> Test written and passed.

#### Construct the opponent (computer) board.
- Add a method to UserInterface which creates a layout of ships in an instance of Game
- Write a test to confirm that UserInterface.genetate_opponent_board stores a list of ship placements inside UserInterface.opponent_game as expected

> Test written and passed.

#### Import shots from opponent game.
- Create a method in Game which takes an opponent_game (instance of Game) as an argument
- It should use opponent_game.shots_made to work out what has been hit or missed, then update some class variable to store that information
- Write a test to check that shots made in opponent_game can be accessed by a player_game and update variable player_game.shots_recieved

> Test written and passed.

#### Implement ship sinking logic in Game.
- Keep track of each ship's hits, and use number of hits vs. length to work out if it has sunk.
- Consider Game.ships_placed = {ship_length: {"pos": [pos1, pos2, pos3, ...], "hits": [hit1, hit2, hit3, ...], "sunk": False}}
- Then use Game.import_shots method to look for hits and sunk ships each time shots are imported
- Write a test that checks the state of the Game.ships_placed dictionary before and after making shots and importing them to the game instance

> Test written and passed

#### Has the player won or lost?
- When importing shots, we reference the opponent game and so can check whether the player has won the game (if the opponent was informed they lost last time they imported shots) - we can store this in a class variable => Game.game_state = "playing", or "won", or "lost"
- When importing shots, check whether all the ships are sunk (in which case player has lost the game!)
- Write a test that checks that the game_state is "lost" when all the player's ships have sunk
- Also check that the game_state is "won" when all opponent's ships have sunk

#### Format player board with hits and misses.
- "X" for a hit, "S" for an unhit ship, "O" for a miss and "." for an unoccupied & unshot cell (see Design Ideas)
- Write a test to check that format board outputs "X" wherever there is a hit, "S" wherever there is an unhit part of a ship, "O" wherever there was a missed shot and "." otherwise
- Testing UserInterface._format_board ... probably not good practice, but calling directly avoids the need to set up the full program in test

> Test written and passed

#### Format opponent board (shown to player) with hits and misses.
- "X" for a hit, "O" for a miss and "." otherwise. No "S" should appear as ships should be hidden from the player
- Write a test to check that format board outputs "X" wherever there is a hit, "O" wherever there was a missed shot and "." otherwise
- Testing UserInterface._format_board ... probably not good practice, but calling directly avoids the need to set up the full program in test

> 

#### Make UserInterface.run capable of handling the full game logic and board outputs.
- Write a test using the Terminal Mock Helper which follows an example game

> 

#### Make UserInterface.run expect two human players.
- Write a test using the Terminal Mock Helper which checks that a second player (p2) is asked to place all their ships after the first player (p1)
- Also test that both p1_game and p2_game have the correct ship placements stored

> 

## Design Ideas

### The Game Board - Hits and Misses
The player game board looks like this: 
```python
..........
...S......
...S......
...S......
..........
....SSSS..
..........
..........
..........
..........  
``` 
Where `S` is a cell occupied by part of a ship.  
The player should see the opponent's board like this:  
```python
...O......
...X......
...X......
..........
..........
......X...
..........
....OO....
..........
..........  
```
Where `X` denotes a hit, and `O` denotes a miss.