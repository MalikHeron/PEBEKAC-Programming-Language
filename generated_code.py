def stringLength(str):
    length = 0
    while str[length] != None:
        length = length + 1
    return length
def main():
    myString = "Hello, World!"
    print(stringLength(myString))
main()