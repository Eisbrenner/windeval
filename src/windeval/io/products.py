import os

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import xarray as xr


def load_product(
    ds1: Dict[str, Union[str, Path]],
    ds2: Dict[str, Union[str, Path]],
    *xarray_args: List[Any],
    path: Optional[Union[str, Path]] = None,
    experimental: bool = False,
    **xarray_kwargs: Dict[str, Any],
) -> Dict[str, xr.Dataset]:
    """Open Dataset

    Parameters
    ----------
    ds1 : dict
        | Dictionary of parameters for first dataset;
        | parameters are:
        |   name : str, optional
        |   file : str, optional
        |   path : str or path_like, optional
    ds2 : dict
        | Dictionary of parameters for second dataset;
        | parameters are:
        |   name : str, optional
        |   file : str, optional
        |   path : str or path_like, optional
    path : str or path_like, optional
    xarray_args : list, optional
    xarray_kwargs : dict, optional
    experimental : bool, optional

    Returns
    -------
    dict
        Dictionary of both input datasets.

    """
    names: List[str] = []
    for x in [ds1, ds2]:
        if x.get("name", None) is not None:
            names.append(str(x["name"]))
        elif x.get("file", None) is not None:
            names.append(Path(x["file"]).stem)
        elif x.get("path", None) is not None:
            names.append(Path(x["path"]).stem)
        else:
            raise ValueError("Unique name, file or path not provided.")
    paths: List[Path] = []
    for i, x in enumerate([ds1, ds2]):
        if x.get("path", None) is not None:
            paths.append(Path(x["path"]))
        elif path is not None:
            paths.append(Path(path))
        else:
            raise ValueError("Paths not provided.")
        if x.get("file", None) is not None:
            paths[i] = Path(paths[i]).joinpath(x["file"])
    for p in paths:
        if not p.exists():
            raise ValueError("File does not exist {}".format(p))
    if experimental:
        ds: Dict[str, xr.Dataset] = {
            n: xr.open_dataset(
                os.path.normpath(paths[i]), *xarray_args, **xarray_kwargs
            )
            for i, n in enumerate(names)
        }
    else:
        raise NotImplementedError(
            "Import of data through Intake is not yet implemented."
        )

    return ds


def export(
    ds: Dict[str, xr.Dataset],
    ds1: Dict[str, Any],
    ds2: Dict[str, Any],
    path: Union[str, Path],
    experimental: bool = False,
    **kwargs: Dict[str, Any],
) -> None:
    """To be implemented."""
    if experimental:
        for k, v in ds.items():
            v.to_netcdf(Path(path).joinpath(k + ".cdf"))
    else:
        raise NotImplementedError("Export of data is not yet implemented.")

    return None


def info(wndpr: Dict[str, xr.Dataset], *args: Any, **kwargs: Dict[str, Any]) -> None:
    """To be implemented."""
    raise NotImplementedError("Info of wind products is not yet implemented.")


def extract(
    wndpr: Dict[str, xr.Dataset], *args: Any, **kwargs: Dict[str, Any]
) -> Dict[str, xr.Dataset]:
    """To be implemented."""
    raise NotImplementedError(
        "Selecting and slicing of dataset is not yet implemented."
    )
