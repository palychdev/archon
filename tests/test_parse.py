from archon.scanner import parse_line


def test_clean_line():
    assert parse_line("/tmp/a.txt: OK") is None


def test_found_line():
    h = parse_line("/tmp/eicar.com: Eicar-Test-Signature FOUND")
    assert h is not None
    assert h.sig == "Eicar-Test-Signature"


def test_inner_archive():
    h = parse_line("/tmp/pack.zip!inner.exe: Win.Trojan FOUND")
    assert h is not None
    assert h.inner != ""
