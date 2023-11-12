# Tests for driving the development of read_time.py
from lib.read_time import *

def test_wrong_type():
    assert read_time(123) == "The input was not text."

def test_empty_string():
    assert read_time("") == "Estimated time to read: 0 min 0 sec"

def test_short_string():
    input = "This string has only six words."
    assert read_time(input) == "Estimated time to read: 0 min 2 sec"

def test_long_string():
    # Input with 420 words.
    input = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Nullam tincidunt odio non pretium sodales. Suspendisse et mauris 
efficitur justo vulputate rhoncus in id lorem. Nulla vel odio vitae urna 
dignissim finibus. Integer luctus quam quis convallis iaculis. Aliquam 
dictum id lorem nec hendrerit. Etiam mauris urna, mollis a nisl in, 
viverra auctor nisl. Nunc purus urna, iaculis a semper sit amet, 
volutpat non ex. Quisque rutrum ipsum quis tellus faucibus porttitor. 
Donec ut odio ex. Curabitur justo nisi, commodo sed augue blandit, 
interdum accumsan lacus. Praesent semper risus et odio suscipit 
vehicula. Quisque suscipit quam ut libero sodales pulvinar. Donec quam 
ante, rhoncus quis felis quis, laoreet ornare libero. Cras dolor sapien, 
luctus sed nulla et, tempor suscipit orci. Ut tincidunt libero urna, ut 
tempus turpis interdum non. Quisque maximus tortor lacus, eget fringilla 
tortor venenatis ut. Vivamus mi metus, tempus vitae tortor vel, posuere 
dignissim nunc. Quisque sollicitudin nec eros et pretium. Nunc in nisl 
ultrices, pulvinar dolor vitae, porttitor augue. Cras in pellentesque 
eros. Fusce a mauris erat. Suspendisse mollis leo sit amet ex rutrum 
auctor. In a luctus ligula, non scelerisque nibh. Nam eget pretium sem, 
ut laoreet massa. Vivamus scelerisque mi a nisi sagittis ultrices. Fusce 
sapien odio, rutrum quis vehicula non, dictum quis ex. In vestibulum, 
justo ut fringilla aliquam, ipsum ex sollicitudin diam, nec ornare mi 
neque eget dolor. Vivamus in urna diam. Duis scelerisque nisi eget erat 
bibendum, a iaculis sem scelerisque. Mauris varius massa rutrum venenatis 
interdum. Quisque at odio auctor, faucibus magna in, molestie neque. 
Quisque sit amet magna fringilla, volutpat libero ut, placerat nibh. 
Nulla lorem tortor, egestas at mi scelerisque, tempus convallis justo. 
Curabitur nec ante aliquam, eleifend lacus eget, maximus felis. Aliquam 
sollicitudin vulputate laoreet. Ut eu bibendum libero, in gravida elit. 
Cras sit amet tortor nisi. Suspendisse vel odio metus. Class aptent 
taciti sociosqu ad litora torquent per conubia nostra, per inceptos 
himenaeos. Nunc velit lectus, dictum ut porttitor in, commodo convallis 
augue. Morbi a vulputate leo, quis sagittis quam. Pellentesque hendrerit 
eu tortor eget dapibus. Nullam vitae urna tincidunt, hendrerit quam 
vitae, auctor turpis. Duis maximus, sem at blandit fermentum, mi mi 
pharetra nulla, ut fringilla mauris justo convallis odio. Ut tristique 
sem ac ex lacinia, ut auctor neque tincidunt. Duis ac diam erat. 
Maecenas ante sem, blandit vel cursus sed, vehicula at metus. Curabitur 
placerat volutpat libero, sed feugiat erat porttitor nec. Aliquam 
efficitur ex orci, eu hendrerit metus mattis sit amet. Mauris interdum 
ultricies vestibulum. Proin placerat ultrices commodo. Phasellus et 
molestie purus. Nulla."""
    assert read_time(input) == "Estimated time to read: 2 min 6 sec"

def test_newlines():
    # text_with_newlines.txt contains 108 paragraphs, each separated by a 
    # blank line. It contains a total of 9620 words.
    with open("./tests/text_with_newlines.txt", "r") as text_file:
        input = text_file.read()
    assert read_time(input) == "Estimated time to read: 48 min 6 sec"

def test_double_spaced():
    # text_double_spaced.txt contains 50 words in 7 sentences. Each sentence
    # ends with a full-stop followed by two whitespace characters (either
    # two spaces "  ", or a space and a newline " \n").
    with open("./tests/text_double_spaced.txt", "r") as text_file:
        input = text_file.read()
    assert read_time(input) == "Estimated time to read: 0 min 15 sec"

