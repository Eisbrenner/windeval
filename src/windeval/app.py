import inspect

import intake
import matplotlib.pyplot as plt
import streamlit as st
import windeval_catalog

from windeval import diagnostics
from windeval.processing import Diagnostics


st.sidebar.markdown("# Load data")
catalog_path = st.sidebar.text_input("Please enter path to the intake data-catalog.")
st.write("# Loaded data sets")
if catalog_path:
    st.markdown("Using default (test) data catalog.")
    cat = windeval_catalog.get_catalog()
else:
    cat = intake.open_catalog(catalog_path)
sel = st.sidebar.multiselect("Select data", list(cat))
if not sel:
    st.markdown("#### Please select datasets from the catalog (sidebar).")

if sel:
    wnd = {key: windeval_catalog.enforce_standard_names(cat[key].read()) for key in sel}

    st.write("Opened wind products:", wnd)

    st.sidebar.markdown("# Select slice")
    st.sidebar.markdown("Not yet implemented.")

    st.write("# Selected slices")
    st.write("Not yet implemented.")

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

    calculate = st.button("Calculate!")
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
