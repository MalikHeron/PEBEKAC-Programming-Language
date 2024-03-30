def fact(n):
    if n == 0:
        return 1
    return n * fact(n - 1)
def main():
    x = 5
    print("The factorial of " , x , "is:" , fact(x))
main()