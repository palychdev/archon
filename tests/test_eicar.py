from archon.scanner import parse_line
from archon.entropy import shannon


EICAR = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"


def test_eicar_string_parses():
    h = parse_line(f"/tmp/eicar.com: {EICAR} FOUND")
    assert h is not None


def test_entropy_runs():
    assert isinstance(shannon(__file__), float)
