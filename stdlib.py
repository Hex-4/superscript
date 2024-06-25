class SuperError(Exception):
    def __init__(self, txt):
        super().__init__(txt)

