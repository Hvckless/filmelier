class Hello:
    world = "undefined"
    def __init__(self):
        self.initial = 1
    def hackpy(self):
        king = input(">")

        if king == "end":
            print("EXECUTED")
            return

        if king == "world":
            print(self.world)
            self.hackpy()
        else:
            self.world = king
            self.hackpy()

    


Hello().hackpy()