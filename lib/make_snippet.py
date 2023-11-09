# Purpose: Take a string as an input, returning the first five words of the
# string followed by "..."
# Example:
# Call: make_snippet("Return the first five words of this sentence.")
# Returns: "Return the first five words..."
def make_snippet(a_string):
    if type(a_string) == type(str()) and a_string.count(" ") <= 4:
        return a_string
    elif type(a_string) == type(str()) and a_string.count(" ") > 4:
        split_string = a_string.split(" ")
        return_string = ""
        for i in range(5):
            return_string += split_string[i] + " "
        return return_string[:-1] + "..."
    else:
        return None
    
