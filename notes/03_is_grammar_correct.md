# Process Log

## Describe the Problem: User Story
> As a user  
> So that I can improve my grammar
> I want to verify that a text starts with a capital letter and ends with a suitable sentence-ending punctuation mark.

## Design the Function Signature
1. Name
    - The name should reflect what the function does.
    - It checks for correct grammar.
    - Let's call it "is_grammar_correct".
2. Parameters
    - The function needs to work on text, so that text should be an input.
    - The text input will be a string, which we can call "text".
    - The rules of the grammar check will not change.
    - So, there are no other parameters.
3. Returns
    - The function should return a Boolean which is True if the grammar check is successful, or false otherwise.
    - This will provide a simple answer to assist the user.
4. Side Effects
    - The function will not interact with files or directories.
    - Nothing will be stored or changed permanently.
    - There should be no unwelcome side effects.

## Create Examples as Tests
1.
    a. Call:
    > is_grammar_check(123)

    b. Returns:
    > TypeError: "Input was not a string."

2. 
    a. Call:
    > is_grammar_check("")  
    
    b. Returns:
    > False

3.
    a. Call:
    > is_grammar_check("A simple string of several words.")

    b. Returns:
    > True

4.
    a. Call:
    > is_grammar_check("Does this work for questions?")

    b. Returns:
    > True

5.
    a. Call:
    > is_grammar_check("Now for an exclamation!")

    b: Returns:
    > True

6.
    a. Call:
    > is_grammar_check("no capital letter.")

    b. Returns:
    > False

## Test-Driving Development
1.
    a. Create test_wrong_type() to check whether the input is a string. ![Image of code for test]()
    - Test fails: no code has been written yet.
    - Write code: ![Image of code to pass test]()
    - Test passes!

    b. Create test_empty_string() to check whether the input is a string. ![Image of code for test]()
    - Test fails: None is returned for any input which does not trigger the TypeError exception.
    - Write code: ![Image of code to pass test]()
    - Test passes!

    c. Create test_full_stop_sentence() to check whether a simple sentence passes the grammar check. ![Image of code for test]()
    - Test fails: all string inputs return False.
    - Write code: ![Image of code to pass test]()
    - Test passes!

    d. Create test_question_mark_sentence() to check whether a question passes the grammar test. ![Image of code for test]()
    - Test fails: only full-stops are tested for in the current code.
    - Write code: ![Image of code to pass test]()
    - Test passes!

    e. Create test_exclamation_mark_sentence() to check whether an exclamation mark passes the grammar test. ![Image of code for test]()
    - Test fails: the exclamation mark has not yet been added to the list of acceptable ending punctuation.
    - Write code: ![Image of code to pass test]()
    - Test passes!

    f. Create test_missing_capital() to check whether the input starts with a capital letter. ![Image of code for test]()
    - Test fails: there is no check for the leading character of the text.
    - Write code: ![Image of code to pass test]()
    - Test passes!
    