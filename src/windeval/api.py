import subprocess

from functools import reduce
from pathlib import Path
from typing import Any, Callable, Dict, KeysView, Optional, Tuple

import numpy as np
import xarray as xr

from .processing import Conversions, Diagnostics


def app() -> None:
    subprocess.run(
        ["streamlit", "run", Path(__file__).resolve().parent.joinpath("app.py")]
    )
    return None


def extract(*args, **kwargs):
    """To be implemented."""
    raise NotImplementedError("Method not implemented: extract.")


def conversions(
    wnd: Dict[Any, xr.Dataset],
    __ds1: Optional[Dict[str, Any]] = None,
    __ds2: Optional[Dict[str, Any]] = None,
    *args: Any,
    **kwargs: Dict[str, Any],
) -> Dict[str, xr.Dataset]:
    """Apply conversions to wind-products.

    Parameters
    ----------
    wnd: dict
        Dictionary containing wind-products as xarray datasets
    ds1: dict, optional
        Dictionary containing method names as keys and method parameters as dictionary
        to be applied to the xarray dataset which name is given via the `name` keyword.
    ds2: dict, optional
        As ds1, for another dataset in `wnd`.
    kwargs: keword_arguments
        key word pairs of methods to be applied to all datasets in `wnd`.

    Returns
    -------
    dict
        Dictionary of wind-products updated with diagnostic results.

    Examples
    --------
    >>> import windeval
    >>> windeval.conversions(
    >>>     windproducts,
    >>>     {"product": "product 1",
    >>>      "height": {"variables": "wind_speed", "from": 2, "to": 10}},
    >>>     {"product": "product 2",
    >>>      "height": {"variables": "wind_speed", "from": 5, "to": 10}},
    >>>     spectra={
    >>>         "variables": "wind_speed",
    >>>         "method":"welch",
    >>>         "nan_handling": "remove",
    >>>         "nperseg": "24"
    >>>     }
    >>> )

    """
    return _processing_interface(
        Conversions, wnd, *_sort_methods(wnd.keys(), [__ds1, __ds2], kwargs), kwargs
    )


def diagnostics(
    wnd: Dict[Any, xr.Dataset],
    __ds1: Optional[Dict[str, Any]] = None,
    __ds2: Optional[Dict[str, Any]] = None,
    *args: Any,
    **kwargs: Dict[str, Any],
) -> Dict[str, xr.Dataset]:
    """Apply diagnostics to wind-products.

    Parameters
    ----------
    wnd: dict
        Dictionary containing wind-products as xarray datasets
    ds1: dict, optional
        Dictionary containing method names as keys and method parameters as dictionary
        to be applied to the xarray dataset which name is given via the `name` keyword.
    ds2: dict, optional
        As ds1, for another dataset in `wnd`.
    kwargs: keword_arguments
        key word pairs of methods to be applied to all datasets in `wnd`.

    Returns
    -------
    dict
        Dictionary of wind-products updated with diagnostic results.

    Examples
    --------
    >>> import windeval
    >>> windeval.diagnostics(
    >>>     windproducts,
    >>>     {"product": "product 1",
    >>>      "mean": {"variables": "wind_speed", "nan_handling": "remove"}},
    >>>     {"product": "product 2",
    >>>      "std": {"variables": "wind_speed", "nan_handling": "replace_mean"}},
    >>>     spectra={
    >>>         "variables": "wind_speed",
    >>>         "method":"welch",
    >>>         "nan_handling": "remove",
    >>>         "nperseg": "24"
    >>>     }
    >>> )

    """

    return _processing_interface(
        Diagnostics, wnd, *_sort_methods(wnd.keys(), [__ds1, __ds2], kwargs), kwargs
    )


def _sort_methods(
    wnd_keys: KeysView[Any], specific_methods: list, general_methods: dict
) -> Tuple[set, Dict[str, set], Dict[str, Dict[str, Any]]]:
    """Separate joined and individual methods."""
    opt = [m for m in specific_methods if m is not None]
    if not all([xi.get("product", None) for xi in opt]):
        raise ValueError(
            "Name of wind product is required to apply methods to specific dataset."
        )
    single_methods_dict = {xi.pop("product"): xi for xi in opt}
    x1 = {key: set(single_methods_dict.get(key, {}).keys()) for key in wnd_keys}
    x2 = reduce(lambda m1, m2: set(m1) | set(m2), x1.values())
    x3 = set(general_methods.keys())
    joined_methods = x3.union(x2) ^ x2
    individual_methods = {key: x3.union(x1[key]) ^ joined_methods for key in x1.keys()}

    return joined_methods, individual_methods, single_methods_dict


def _processing_interface(
    processing_callable: Callable,
    wnd: Dict[str, xr.Dataset],
    joined_methods: set,
    individual_methods: Dict[str, set],
    single_methods_dict: Dict[str, Dict[str, Any]],
    kwargs: Dict,
) -> Dict[Any, xr.Dataset]:
    """Calls processing classes and functions from the processing module."""
    for method in joined_methods:
        for variable in list(np.array(kwargs[method].get("variables")).flat):
            wnd = getattr(processing_callable, method)(
                wnd,
                variable,
                method_args=kwargs[method].get("args"),
                method_kwargs={
                    k: kwargs[method][k]
                    for k in kwargs[method].keys()
                    if k not in ["args", "variables"]
                },
            )
    for product, methods in individual_methods.items():
        for method in methods:
            kwgs = {**kwargs.get(method, {}), **single_methods_dict[product]}[method]
            for variable in list(np.array(kwgs.get("variables")).flat):
                wnd = getattr(processing_callable, method)(
                    wnd,
                    variable,
                    product=product,
                    method_args=kwgs.get("args"),
                    method_kwargs={
                        k: kwgs[k]
                        for k in kwgs.keys()
                        if k not in ["args", "variables"]
                    },
                )

    return wnd
