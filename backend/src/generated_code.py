def fact(n):
    if n == 0:
        return 1
    else:
        x = fact(n - 1)
        return n * x
    return 0
print(fact(6))