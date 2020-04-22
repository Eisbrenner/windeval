import pytest
import windeval.io.reports as reports


def test_report(X):
    with pytest.raises(NotImplementedError):
        reports.report({"ds": X})
