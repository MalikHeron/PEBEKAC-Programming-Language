def fact(n):
    if n == 0:
        return 1
    return n * fact(n - 1)
def main():
    x = fact(5)
    print("The factorial of " , x , "is:" , fact(5))
main()