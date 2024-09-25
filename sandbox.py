x = "dog"

class A:
    x = "cat"

class B(A):
    x = "ferret"
    def __init__(self):
        x = "tomato"

b = B()
print(b.x)