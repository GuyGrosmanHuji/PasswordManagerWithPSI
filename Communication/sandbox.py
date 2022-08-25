class Test:
    def __init__(self):
        self.switch = False

    def __enter__(self):
        if self.switch:
            return self
        x = Test()
        x.switch = True
        return x.__enter__()

    def __exit__(self, *args):
        if self.switch:
            print("You exited!")
        print("You exited, Twice!")


with Test() as t:
    pass
