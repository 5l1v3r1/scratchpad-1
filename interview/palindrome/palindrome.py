#!/usr/bin/env python3

def is_palindrome(target):
    clean = "".join(c.lower() for c in target if c.isalnum())
    return clean == "".join(reversed(clean))

if __name__ == "__main__":
    import sys
    assert is_palindrome("A Toyota.") == True
    print(is_palindrome(sys.argv[1]))
