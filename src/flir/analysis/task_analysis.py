"""Tasks running the core analyses."""

import pandas as pd
import pytask
import pickle

from flir.config import BLD, BASIS
from flir.analysis.estimation import flir


for basis in BASIS:

    kwargs = {
        "basis": basis,
        "produces": BLD / "analysis" / f"{basis}_none.pkl",
    }

    @pytask.mark.wip
    @pytask.mark.depends_on(
        {
            "consumption": BLD / "data" / "consumption_cleaned.csv",
            "LBMP": BLD / "data" / "LBMP_cleaned.csv",
            "wind": BLD / "data" / "wind_cleaned.csv",
        }
    )
    @pytask.mark.task(id=basis, kwargs=kwargs)
    def estimation_flir_none(depends_on, produces, basis):
        consumption = pd.read_csv(depends_on["consumption"])
        LBMP = pd.read_csv(depends_on["LBMP"])
        wind = pd.read_csv(depends_on["wind"])
        result = flir(consumption, LBMP, wind, 11, basis, "none")

        with open(produces, "wb") as f:
            pickle.dump(result, f, protocol=pickle.HIGHEST_PROTOCOL)


for basis in BASIS:

    kwargs = {
        "basis": basis,
        "produces": BLD / "analysis" / f"{basis}_second_derivative.pkl",
    }

    @pytask.mark.wip
    @pytask.mark.depends_on(
        {
            "consumption": BLD / "data" / "consumption_cleaned.csv",
            "LBMP": BLD / "data" / "LBMP_cleaned.csv",
            "wind": BLD / "data" / "wind_cleaned.csv",
        }
    )
    @pytask.mark.task(id=basis, kwargs=kwargs)
    def estimation_flir_second_derivative(depends_on, produces, basis):
        consumption = pd.read_csv(depends_on["consumption"])
        LBMP = pd.read_csv(depends_on["LBMP"])
        wind = pd.read_csv(depends_on["wind"])
        result = flir(consumption, LBMP, wind, 11, basis, "second_derivative")

        with open(produces, "wb") as f:
            pickle.dump(result, f, protocol=pickle.HIGHEST_PROTOCOL)


for basis in BASIS:

    kwargs = {
        "basis": basis,
        "produces": BLD / "analysis" / f"{basis}_harmonic.pkl",
    }

    @pytask.mark.wip
    @pytask.mark.depends_on(
        {
            "consumption": BLD / "data" / "consumption_cleaned.csv",
            "LBMP": BLD / "data" / "LBMP_cleaned.csv",
            "wind": BLD / "data" / "wind_cleaned.csv",
        }
    )
    @pytask.mark.task(id=basis, kwargs=kwargs)
    def estimation_flir_harmonic(depends_on, produces, basis):
        consumption = pd.read_csv(depends_on["consumption"])
        LBMP = pd.read_csv(depends_on["LBMP"])
        wind = pd.read_csv(depends_on["wind"])
        result = flir(consumption, LBMP, wind, 11, basis, "harmonic")

        with open(produces, "wb") as f:
            pickle.dump(result, f, protocol=pickle.HIGHEST_PROTOCOL)
