s = "abcdefghij"

def print_recursive_string(s, p = ""):
    if len(s) == 0:
        return ""
    elif len(s) == 1:
        print(p + s)
    else:
        for i in range(len(s)):
            print_recursive_string(s[0:i] + s[i+1:], p + s[i])

print_recursive_string(s)
