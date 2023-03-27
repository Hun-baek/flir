"""Tasks running the results formatting (tables, figures)."""

import pandas as pd
import numpy as np
import pickle
import pytask

from flir.config import BLD, BASIS
from flir.final.plot import plot_estimated_function

for basis in BASIS:

    kwargs = {
        "basis": basis,
        "produces": BLD / "figures" / f"{basis}_estimation.png",
    }

    @pytask.mark.wip
    @pytask.mark.depends_on(
        {
            "none": BLD / "analysis" / f"{basis}_none.pkl",
            "secondD": BLD / "analysis" / f"{basis}_constraint.pkl",
            "harmonic": BLD / "analysis" / f"{basis}_harmonic.pkl",
        },
    )
    @pytask.mark.task(id=basis, kwargs=kwargs)
    def task_plot_estimation(depends_on, basis, produces):
        with open(depends_on["none"], "rb") as f:
            data_none = pickle.load(f)
        with open(depends_on["secondD"], "rb") as f:
            data_secondD = pickle.load(f)
        with open(depends_on["harmonic"], "rb") as f:
            data_harmonic = pickle.load(f)

        dict_varphi = {
            f"{basis}": data_none["varphi"],
            f"{basis}_constraint": data_secondD["varphi"],
            f"{basis}_harmonic": data_harmonic["varphi"],
            "grid": np.linspace(0, 23, 101),
        }

        data = pd.DataFrame(dict_varphi)

        fig = plot_estimated_function(data, basis)
        fig.write_image(produces)
