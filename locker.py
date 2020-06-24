class GIL():
    def __init__(self):
        self.GIL = True

    def UpdateState(self, update):
        self.GIL = update

    def ReturnState(self) -> bool:
        return self.GIL


def lock():
    """Locks the lock."""
    instance.UpdateState(True)


def unlock():
    """Unlocks the lock."""
    instance.UpdateState(False)


def islocked() -> bool:
    """Returns the locks state."""
    return instance.ReturnState()


instance = GIL()

