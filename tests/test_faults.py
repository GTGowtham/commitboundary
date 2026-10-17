from faults import timeoutAfterCommit

def test_timeout_trigger_only_once():
      fault=timeoutAfterCommit()
      assert fault.should_timeout() ==True
      assert fault.should_timeout() ==False
      assert fault.should_timeout() ==False