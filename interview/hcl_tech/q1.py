from q2 import timed

# 1. Fibonacci series.


@timed("Fibonacci Series")
def fib(n, memo={}):
    if n in memo:
        return memo[n]
    memo[n] = n if n < 2 else fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]


print(fib(1_00))
