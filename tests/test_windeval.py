from windeval import __version__


def test_version():
    assert __version__ == "2020.1"


def test_all():
    """Test that __all__ contains only names that are actually exported."""
    import windeval

    missing = set(n for n in windeval.__all__ if getattr(windeval, n, None) is None)
    assert missing.__len__() == 0, "__all__ contains unresolved names: {}".format(
        ", ".join(missing)
    )
