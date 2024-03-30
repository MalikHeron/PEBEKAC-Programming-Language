def isPalindrome(str):
    if str == None:
        return False
    length = len(str)
    i = 0
    j = length - 1
    while i < j:
        if str[i] != str[j]:
            return False
    return True
def main():
    str = "racecar"
    if isPalindrome(str):
        print("The string is a palindrome")
    else:
        print("The string is not a palindrome")
main()