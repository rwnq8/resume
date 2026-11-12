"""STYLE-LINT-1 trips on machine-written prose and passes the resume and plain writing."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import style_lint
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assert len(style_lint.lint("I am passionate about leveraging cutting-edge AI \u2014 a robust, seamless approach.")) >= 4
assert style_lint.lint("I ran the model at DVRPC for three years. It broke twice; both times the input network was wrong.") == []
assert style_lint.lint(open(os.path.join(ROOT, "RESUME.md"), encoding="utf-8").read()) == [], "RESUME.md has machine-writing tells"
print("test_style_lint: ok")
