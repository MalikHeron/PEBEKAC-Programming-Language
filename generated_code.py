def is_valid_number(n):
    n = -5
    if n <= 0:
        return False
    if n > 0:
        return True
    return False
def factorial(n):
    if is_valid_number(n):
        print("Valid input")
    else:
        print("Invalid")
factorial(5)