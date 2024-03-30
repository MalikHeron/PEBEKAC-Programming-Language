def isPalindrome(str):
    length = len(str)
    i = 0
    j = length - 1
    while i < j:
        if str[i] != str[j]:
            return False
        i = i + 1
        j = j - 1
    return True
def main():
    str = "racecar"
    if isPalindrome(str):
        print("The string is a palindrome.")
    else:
        print("The string is not a palindrome.")
main()