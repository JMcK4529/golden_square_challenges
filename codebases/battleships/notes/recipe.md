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
Already implemented.

```
As a player
So the game is more fun to play
I would like a nice command line interface that lets me enter ship positions and
shots using commands.
```
Already implemented.

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
Implemented in Game.place_ship method.

```
As a player
So that I can have a coherent game
I would like ships to be constrained not to overlap
```
Not yet implemented.

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
- Asking for a different input means changing Game.place_ship so it validates inputs, and using a try/except in UserInterface._prompt_for_ship_placement so that it only proceeds once a valid input is taken

> This is now passing tests for the first ship placement.  
> Will have to expand test when additional ships can be placed. Expect passes because UserInterface._prompt_for_ship_placement has been changed, and this same method can be called to get future ship positions.

#### 