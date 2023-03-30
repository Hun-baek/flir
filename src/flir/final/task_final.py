"""Tasks running the results formatting (tables, figures)."""

import pandas as pd
import numpy as np
import pickle
import pytask

from flir.config import BLD, BASIS, PAPER_DIR, GROUP, CONSTRAINT
from flir.final.plot import plot_estimated_function, plot_hourly, plot_GCV

for basis in BASIS:

    kwargs = {
        "basis": basis,
        "produces": BLD / "figures" / f"{basis}_estimation.png",
    }

    @pytask.mark.depends_on(
        {
            "none": BLD / "analysis" / f"{basis}_none.pkl",
            "secondD": BLD / "analysis" / f"{basis}_second_derivative.pkl",
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


for constraint in CONSTRAINT:

    kwargs = {
        "produces": BLD / "figures" / f"fourier_{constraint}_gcv.png",
    }

    @pytask.mark.depends_on({"data": BLD / "analysis" / f"fourier_{constraint}.pkl"})
    @pytask.mark.task(kwargs=kwargs)
    def task_plot_gcv(depends_on, produces):
        with open(depends_on["data"], "rb") as f:
            data = pickle.load(f)

        fig = plot_GCV(data)
        fig.write_image(produces)


for group in GROUP:

    kwargs = {
        "group": group,
        "produces": BLD / "figures" / f"{group}_hourly.png",
    }

    @pytask.mark.depends_on(
        {
            "data": BLD / "data" / f"{group}_cleaned.csv",
        },
    )
    @pytask.mark.task(id=group, kwargs=kwargs)
    def task_plot_hourly(depends_on, group, produces):
        data = pd.read_csv(depends_on["data"])

        plot_hourly(data, group, produces)


@pytask.mark.latex(
    script=PAPER_DIR / "flir.tex",
    document=PAPER_DIR / "flir.pdf",
)
def task_compile_latex_docuemnt():
    pass
