import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims_check
c = [{"ref": "a", "marker": "X claim"}, {"ref": "b", "marker": "Y claim"}]
bad, open_ = claims_check.check(c, {"a": "no", "b": "yes"}, "has X claim and Y claim")
assert [x["ref"] for x in bad] == ["a"] and open_ == []
bad, open_ = claims_check.check(c, {"a": "no"}, "has Y claim only")
assert bad == [] and open_ == ["b"]
print("test_claims_check: ok")
