class timeoutAfterCommit:
      def __init__(self):
            self.triggered=False
      
      def should_timeout(self):
            if not self.triggered:
                  self.triggered=True
                  return True
            return False


if __name__ == "__main__":
      r1=timeoutAfterCommit()
      print(r1.should_timeout())
      print(r1.should_timeout())
      print(r1.should_timeout())