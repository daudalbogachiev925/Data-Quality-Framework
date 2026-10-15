from src.rules import not_null, is_positive, in_range, is_unique, matches_regex

def test_not_null():
    assert not_null(1) and not_null("a")
    assert not not_null(None) and not not_null("")

def test_is_positive():
    assert is_positive(1.5)
    assert not is_positive(-1)
    assert not is_positive("abc")

def test_is_unique():
    assert is_unique([1, 2, 3])
    assert not is_unique([1, 1, 2])

def test_regex():
    rx = matches_regex(r"^\d+$")
    assert rx("123")
    assert not rx("abc")
