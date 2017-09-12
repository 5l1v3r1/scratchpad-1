#!/usr/bin/env python3.6
"""
Use the inspect module to write a decorator for executing a callback on an
argument to the wrapped function.
"""

import inspect
from functools import wraps


def autocall(callback, param_name='the_name'):

    def decorator(f):
        sig = inspect.signature(f)

        if param_name not in sig.parameters:
            # This is just so the exception occurs when the function is wrapped,
            # rather than when it's called, since the error is more relevant to
            # the decorator than to the wrapped function.
            raise ValueError(f"Wrapped function has no parameter '{param_name}'")

        @wraps(f)
        def wrapper(*args, **kwargs):
            bound_arguments = sig.bind(*args, **kwargs)
            bound_arguments.apply_defaults()

            value = bound_arguments.arguments[param_name]

            callback(value)

            return f(*args, **kwargs)

        return wrapper

    return decorator


def print_callback(val):
    print(f"Value is {val}")


@autocall(print_callback, param_name='x')
def function(w, x, y=3, z=4):
    print(w, x, y, z)


if __name__ == "__main__":
    function(1, 2, 3, 4)
    function(x=2, w=1)
    function(y=3, x=2, w=1)
