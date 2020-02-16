
"""
    This is a solution to the problem:

    In a matrix of letters, detect any 2x2 squares of vowels

    We operate using an array of arrays, and print out the "top-left" position
    of the square
"""

""" Simple representation of a matrix """
m = [
    ["a", "t", "y", "d", "n"],
    ["f", "t", "w", "o", "a"],
    ["a", "e", "l", "i", "e"],
    ["o", "a", "u", "a", "u"],
    ["q", "e", "i", "u", "i"],
]

def is_vowel(c):
    """ return whether passed char is a vowel """
    assert isinstance(c, str)
    for v in ["a", "e", "i", "o", "u" ]:
        if c == v:
            return True
    return False

def has_vowel_at(m, i, j):
    """ check if a matrix array has a vowel at a specific position

        @NOTE we are a bit forgiving on positions outside of the matix boundaries
            because our matrix representation is not ideal, and could easily be
            missing "columns" in a "row"
    """
    if i < len(m) and j < len(m[i]):
        return is_vowel(m[i][j])
    return False

"""
    Range across all elements of the matrix, as columns in a row, checking if
    each element is the top-left of a vowel square.
"""
for i in range(len(m)-1):
    for j in range(len(m[i])-1):
        if (is_vowel(m[i][j])
                and has_vowel_at(m, i+1, j)
                and has_vowel_at(m, i, j+1)
                and has_vowel_at(m, i+1, j+1)):
            print("Found at %i, %i" % (i, j))
