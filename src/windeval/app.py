import inspect

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import streamlit as st
import xarray as xr

from windeval import diagnostics, load_product
from windeval.processing import Diagnostics


def main():
    app = App()

    app.select_page()

    st.sidebar.markdown("# Actions")
    calculate = st.sidebar.button("Calculate")
    if calculate:
        st.write("# Plots and results")
        _calculate(app.data, app.variable, app.global_diag)
        st.pyplot()

    return None


def _setup_paths():
    path1 = st.sidebar.text_input("Please enter path to the first data set.")
    path2 = st.sidebar.text_input("Please enter path to the second data set.")

    return [path1, path2]


def _check_paths(paths):
    fmap = {0: "First", 1: "Second"}
    wait = [True, True]
    for i in range(2):
        if not Path(paths[i]).exists() or not paths[i]:
            paths[i] = (
                Path(__file__)
                .resolve()
                .parent.parent.parent.joinpath(
                    "tests/test_data/station_{}.cdf".format(i + 1)
                )
            )
            if Path(paths[i]).exists():
                st.write(
                    "WARNING: {} file does not exist or none given."
                    " Using test path:\n\n".format(fmap[i]),
                    paths[i],
                )
        if Path(paths[i]).exists():
            wait[i] = False
        else:
            st.write("WARNING: {} file does not exist or none given.".format(fmap[i]))

    return paths, wait


def _calculate(wnd, variable, global_diag):
    diagnostics(wnd, **global_diag)
    for k in wnd.keys():
        plt.semilogx(wnd[k][variable + "_power_spectral_density"])
    plt.legend(wnd.keys())
    plt.title("PSD: power spectral density")
    plt.xlabel("Frequency")
    plt.ylabel("Power")
    plt.tight_layout()
    plt.grid()

    return None


class _Pages:

    _page = "page01_data_source"

    def _show_page(self):
        getattr(self, self._page)()

        return None

    @staticmethod
    def _pages():
        return sorted([page for page in dir(_Pages) if page[0] != "_"])

    def page01_data_source(self, app):
        st.sidebar.markdown("# Data Source")
        app.paths = _setup_paths()
        app.paths, app.wait = _check_paths(app.paths)
        if not any(app.wait):
            _load_ds(app)

        return None

    def page02_slice_selection(self, app):
        st.sidebar.markdown("# Slice Selection")

    def page03_calculations(self, app):
        st.sidebar.markdown("# Calculations")
        app.variable = st.sidebar.selectbox(
            "Select variable:",
            sorted(list(app.data[list(app.data.keys())[0]].data_vars)),
        )
        diag = st.sidebar.selectbox(
            "Select method:",
            [
                a[0]
                for a in inspect.getmembers(Diagnostics)
                if not (a[0].startswith("__") and a[0].endswith("__"))
            ],
        )
        assert getattr(Diagnostics, diag) is not None
        app.global_diag = {
            diag: {"variables": app.variable, "method": "welch", "nperseg": 26}
        }

        return None


class App:

    # initialize session variables
    pages = _Pages()
    paths = [
        Path(__file__)
        .resolve()
        .parent.parent.parent.joinpath("tests/test_data/station_{}.cdf".format(i + 1))
        for i in range(2)
    ]
    _data: Optional[xr.Dataset] = None
    wait = [False, False]
    variable = None
    global_diag = None

    @property
    def data(self):
        if get(self._data, None) is None:
            ds = load_product(*[{"path": p} for p in self.paths], experimental=True)
        else:
            ds = self._data
        return ds

    def select_page(self):
        pages = {
            " ".join(page.split("_")[1:]).title(): page for page in self.pages._pages()
        }
        page = st.selectbox("", list(pages.keys()))
        getattr(self.pages, pages[page])(self)

        return None


if __name__ == "__main__":
    main()
