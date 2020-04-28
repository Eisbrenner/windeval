import pytest
import xarray as xr

from windeval import conversions, diagnostics, extract, load_product


def test_extract():
    with pytest.raises(NotImplementedError):
        extract()


def test_conversions(path_to_test_data):
    wnd = load_product(
        dict(file="station_1.cdf"),
        dict(file="station_2.cdf"),
        path=path_to_test_data,
        experimental=True,
    )
    wnd = conversions(wnd)


def test_diagnostics(path_to_test_data):
    wnd = load_product(
        dict(file="station_1.cdf"),
        dict(file="station_2.cdf"),
        path=path_to_test_data,
        experimental=True,
    )
    spectra_kwargs = dict(variables="WS_401", method="welch", nperseg=26)
    return_wnd = diagnostics(wnd, spectra=spectra_kwargs)
    assert isinstance(return_wnd, dict)
    for data in return_wnd.values():
        assert isinstance(data, xr.Dataset)
        assert spectra_kwargs["variables"] + "_power_spectral_density" in data.data_vars

    with pytest.raises(ValueError):
        diagnostics(wnd, dict(spectra=spectra_kwargs))

    product = "station_1"
    return_wnd = diagnostics(wnd, dict(product=product, spectra=spectra_kwargs))
    assert isinstance(return_wnd, dict)
    assert (
        spectra_kwargs["variables"] + "_power_spectral_density"
        in return_wnd[product].data_vars
    )
    assert isinstance(
        return_wnd[product][spectra_kwargs["variables"] + "_power_spectral_density"],
        xr.DataArray,
    )
