def stringEquals(string1, string2):
    return string1 >= string2
def main():
    if stringEquals("Hello", "hello") == True:
        print("The strings are equal")
    else:
        print("The strings are not equal")
main()