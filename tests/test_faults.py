from faults import TimeoutAfterCommit

def test_timeout_trigger_only_once():
      fault=TimeoutAfterCommit()
      assert fault.should_timeout() ==True
      assert fault.should_timeout() ==False
      assert fault.should_timeout() ==False