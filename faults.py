class TimeoutAfterCommit:
    def __init__(self):
        self.triggered = False

    def should_timeout(self) -> bool:
        if not self.triggered:
            self.triggered = True
            return True
        return False


if __name__ == "__main__":
    fault = TimeoutAfterCommit()
    print(fault.should_timeout())
    print(fault.should_timeout())
    print(fault.should_timeout())
