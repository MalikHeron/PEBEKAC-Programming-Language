def main():
    x = 10
    print("x inside main: " , x)
    if True:
        x = 15
        print("x inside if: " , x)
    print("x inside main after if: " , x)
    def add(a, b):
        x = 3
        print("x inside add: " , x)
    add(3, 2)
def scopeTest():
    x = 20
    print("x inside scopeTest: " , x)
scopeTest()
main()
print("x outside of scope: " , x)