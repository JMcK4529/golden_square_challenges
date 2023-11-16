# Music Tracker Class Design Recipe

## 1. Describe the Problem

_Put or write the user story here. Add any clarifying notes you might have._

> As a user
> So that I can keep track of my music listening
> I want to add tracks I've listened to and see a list of them.

## 2. Design the Class Interface

_Include the initializer, public properties, and public methods with all parameters, return values, and side-effects._

```python
class MusicTracker:
    # User-facing properties:
    #   

    def __init__(self):
        # Parameters:
        #   None
        # Side effects:
        #   Creates a class variable: self.track_list = []
        #   self.track_list will have tracks added to it
        pass # No code here yet

    def add_track(self, track_name):
        # Parameters:
        #   track_name: a string containing the name of the track
        # Returns:
        #   Nothing
        # Side-effects:
        #   Stores the track_name in the self object
        pass # No code here yet

    def list_tracks(self):
        # Parameters:
        #   None
        # Returns:
        #   A list of all tracks added so far
        # Side-effects:
        #   None
        pass # No code here yet
```

## 3. Create Examples as Tests

_Make a list of examples of how the class will behave in different situations._

``` python
# __init__(self)
"""
When instance created:
#init creates an empty list (self.track_list)
"""
my_music = MusicTracker() # my_music.track_list = []

# add_track(self, track_name)
"""
Given a non-string track_name
#add_track raises a TypeError
"""
my_music = MusicTracker()
my_music.add_track(123) # raises a TypeError with the message "track_name must be a string"

"""
Given an empty string track_name
#add_track raises a ValueError
"""
my_music = MusicTracker()
my_music.add_track("") # raises a ValueError with the message "Empty string cannot be a track_name"

"""
Given the name of a track_name
#add_track adds the track_name to self.track_list
"""
my_music = MusicTracker()
my_music.add_track("Bohemian Rhapsody") # returns nothing, but now self.track_list = ["Bohemian Rhapsody"]

# list_tracks(self)
"""
When called:
#list_tracks returns the full track list
"""
my_music = MusicTracker()
my_music.add_track("Bohemian Rhapsody")
my_music.add_track("Yellow Submarine")
my_music.list_tracks() # => ["Bohemian Rhapsody", "Yellow Submarine"]
```

_Encode each example as a test. You can add to the above list as you go._

## 4. Implement the Behaviour

_After each test you write, follow the test-driving process of red, green, refactor to implement the behaviour._