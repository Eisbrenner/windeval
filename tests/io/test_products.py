from pathlib import Path

import pytest
import windeval.io.products as products


def test_load_product(path_to_test_data):
    ds1 = dict(name="1", path=path_to_test_data.joinpath("field_1.cdf"))
    ds2 = dict(file="field_2.cdf")
    wnd = products.load_product(ds1, ds2, path=path_to_test_data, experimental=True)
    assert "1" in wnd.keys()
    assert "field_2" in wnd.keys()
    wnd = products.load_product(
        ds1, dict(path=path_to_test_data.joinpath("station_1.cdf")), experimental=True
    )
    assert "station_1" in wnd.keys()
    with pytest.raises(ValueError):
        products.load_product(dict(name=""), dict(name=""))
    with pytest.raises(ValueError):
        products.load_product(ds1, ds2, path="/wrong/path")
    with pytest.raises(ValueError):
        products.load_product(dict(), ds2)
    with pytest.raises(NotImplementedError):
        products.load_product(ds1, ds2, path=path_to_test_data)


def test_export(path_to_test_data):
    ds = [dict(name=i, file="station_" + i + ".cdf") for i in "12"]
    products.export(
        products.load_product(*ds, path=path_to_test_data, experimental=True),
        dict(),
        dict(),
        Path.cwd(),
        experimental=True,
    )
    for i in "12":
        assert Path.cwd().joinpath(i + ".cdf").exists()
        Path.cwd().joinpath(i + ".cdf").unlink()
        assert not Path.cwd().joinpath(i + ".cdf").exists()
    with pytest.raises(NotImplementedError):
        products.export(dict(), dict(), dict(), str())


def test_info(X):
    with pytest.raises(NotImplementedError):
        products.info({"ds": X})


def test_extract(X):
    with pytest.raises(NotImplementedError):
        products.extract({"ds": X})
