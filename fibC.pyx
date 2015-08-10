# Cython fibonacci 

def fib(n):
    """Return the Fibonacci series up to n."""
    a, b = 0, 1
    while b < n:
        #print b,
        yield b
        a, b = b, a + b