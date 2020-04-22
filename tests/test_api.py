import pytest
import xarray as xr

from windeval import load_product
from windeval.api import conversions, diagnostics


def test_conversions():
    with pytest.raises(NotImplementedError):
        conversions()


def test_diagnostics(path_to_test_data):
    wnd = load_product(
        dict(file="station_1.cdf"),
        dict(file="station_2.cdf"),
        path=path_to_test_data,
        experimental=True,
    )
    var = "WS_401"
    return_wnd = diagnostics(wnd, spectra=dict(method="welch", variables=var))
    assert isinstance(return_wnd, dict)
    for data in return_wnd.values():
        assert isinstance(data, xr.Dataset)
        assert var + "_power_spectral_density" in data.data_vars

    with pytest.raises(ValueError):
        diagnostics(wnd, dict(spectra=dict(method="welch", variables=var)))

    product = "station_1"
    return_wnd = diagnostics(
        wnd, dict(product=product, spectra=dict(method="welch", variables=var))
    )
    assert isinstance(return_wnd, dict)
    assert var + "_power_spectral_density" in return_wnd[product].data_vars
    assert isinstance(
        return_wnd[product][var + "_power_spectral_density"], xr.DataArray
    )
