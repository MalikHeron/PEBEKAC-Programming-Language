def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
def main():
    n = 4
    print("Factorial of" , n , "is" , factorial(n) , "\n;")
main()