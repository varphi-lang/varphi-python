import io
import sys
import re
from contextlib import redirect_stdout

from varphi_python import VarphiToPythonCompiler
from varphi_devkit import compile_varphi

def test_add_one():
    program = """
    q0 1 q0 1 R
    q0 0 q1 1 R
    """

    compiler = VarphiToPythonCompiler()
    result = compile_varphi(program, compiler)

    fake_stdin = io.StringIO("11\n")
    buf = io.StringIO()

    orig_stdin = sys.stdin
    try:
        sys.stdin = fake_stdin
        with redirect_stdout(buf):
            exec(result, {"__name__": "__main__"})
    finally:
        sys.stdin = orig_stdin

    out = buf.getvalue()
    m = re.findall(r"[01]+", out)
    assert m and m[-1] == "1110", f"Expected '1110', got {m[-1] if m else out!r}\nFull output:\n{out}"
