import pytest

from windeval import reports


def test_report(X):
    with pytest.raises(NotImplementedError):
        reports.report({"ds": X})
