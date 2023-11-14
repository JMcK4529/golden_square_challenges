# Process Log

## Describe the Problem: User Story
> As a user
> So that I can keep track of tasks
> I want to check whether a text contains the string #TODO

## Design the Function Signature
1. Name
    - The name should reflect what the function does.
    - It should search through text and check for "#TODO".
    - Let's call it "contains_todo".
2. Parameters
    - The function needs to work on text, so that text should be an input.
    - The input will be a string, which we can call "text".
3. Returns
    - The function should return a Boolean which is True if the text contains "#TODO", False otherwise.
4. Side Effects
    - The input text is not saved, so could be lost if not stored somewhere else.

## Create Examples as Tests
1.
    a. Call:
    > contains_todo(123)

    b. Returns:
    > TypeError: "The input was not a string."

2. 
    a. Call:
    > contains_todo("")
    
    b. Returns:
    > False

3.
    a. Call:
    > contains_todo("#TODO")

    b. Returns:
    > True

4.
    a. Call:
    > contains_todo("This string is a #TODO reminder.")

    b. Returns:
    > True

5.
    a. Call:
    > contains_todo("This string does not contain the phrase!")


## Test-Driving Development
1.
    a. Create test_wrong_type() to check whether the function differentiates for strings.
    - Test fails: no code has been written yet.
    - Write code: done.
    - Test passes.

    b. Create test_empty_string() to check if the function returns False for a string not containing #TODO.
    - Test fails: function returns None for any string input.
    - Write code: done.
    - Test passes.

    c. Create test_simple_todo() to check if the function returns True for a simple string containing #TODO.
    - Test fails: function returns False for all string inputs.
    - Write code: done
    - Test passes.

    d. Create test_complex_todo() to check if the function retruns True for a more complex string containing #TODO.
    - Test already passes!

    e. Create test_not_a_todo() to check if the function returns False for a more complex string not containing #TODO.
    - Test already passes!