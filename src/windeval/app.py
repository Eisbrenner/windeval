import inspect

from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st

from windeval import diagnostics, load_product
from windeval.processing import Diagnostics


st.sidebar.markdown("# Load data")
path1 = st.sidebar.text_input("Please enter path to the first data set.")
path2 = st.sidebar.text_input("Please enter path to the second data set.")
paths = [path1, path2]

st.write("# Loaded data sets")
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
                "WARNING: {} file does not exist or none given. Using test path:\n\n".format(
                    fmap[i]
                ),
                paths[i],
            )
    if Path(paths[i]).exists():
        wait[i] = False
    else:
        st.write("WARNING: {} file does not exist or none given.".format(fmap[i]))

if not any(wait):
    wnd = load_product(*[{"path": p} for p in paths], experimental=True)
    st.write("Opened wind products:", wnd)

    st.sidebar.markdown("# Select slice")
    st.write("# Selected slices")

    st.sidebar.markdown("# Select diagnostic method")
    st.write("# Result")

    variable = st.sidebar.selectbox(
        "Select variable:", list(wnd[list(wnd.keys())[0]].data_vars)
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
    global_diag = {diag: {"variables": variable, "method": "welch", "nperseg": 26}}

    calculate = st.button("Calculate")
    if calculate:
        diagnostics(wnd, **global_diag)
        for k in wnd.keys():
            plt.semilogx(wnd[k][variable + "_power_spectral_density"])
        plt.legend(wnd.keys())
        plt.title("PSD: power spectral density")
        plt.xlabel("Frequency")
        plt.ylabel("Power")
        plt.tight_layout()
        plt.grid()
        st.pyplot()
