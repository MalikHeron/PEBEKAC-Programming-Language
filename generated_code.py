def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)
def main():
    print(factorial(5))
    return 0
main()