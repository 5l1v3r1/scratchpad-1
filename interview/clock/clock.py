#!/usr/bin/env python3

def clock(time):
    """
    clock(time) -> bool

    Find the angle between the hour hand an minute hand given the digital time.

    >>> clock("2:50")
    145.0
    """
    hour, minute = map(int, time.split(":"))

    # minute hand (degrees from 12)
    # each minute that passes, the minute hand
    # moves 6 degrees
    min_deg = minute * 6

    # hour hand (degrees from 12)
    # each minute that passes, the hour hand
    # moves 0.5 degrees
    hour_deg = ((hour % 12) * 60 + minute) * 0.5

    degrees = abs(hour_deg - min_deg)

    # return the acute angle
    return min(degrees, 360-degrees)

if __name__ == "__main__":
    import sys
    assert clock("2:50") == 145.0
    print(clock(sys.argv[1]))
