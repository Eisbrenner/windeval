import pytest
import windeval.plotting as plotting

from windeval import diagnostics


def test_plot(X):
    plotting.plot({"ds": X}, "eastward_wind")
    with pytest.raises(NotImplementedError):
        plotting.plot(False)
    with pytest.raises(NotImplementedError):
        plotting.plot({"ds": X}, "eastward_wind", dataset=[])

    wnd = dict(ds1=X, ds2=X)
    wnd = diagnostics(wnd, spectra=dict(variables="eastward_wind", method="welch"))

    plotting.plot(wnd, "eastward_wind_power_spectral_density")
