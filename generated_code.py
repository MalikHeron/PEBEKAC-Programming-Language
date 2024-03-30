def fact(n):
    if n == 0:
        return 1
    return n * fact(n - 1)
def main():
    m = 5.0
    x = fact(5)
    print("The factorial of " , x , "is:" , fact(x))
main()