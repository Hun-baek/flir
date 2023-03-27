"""Tasks running the core analyses."""

import pandas as pd
import pytask
import pickle

from flir.config import BLD, BASIS
from flir.analysis.estimation import flir

# @pytask.mark.depends_on(
#     {
#         "scripts": ["model.py", "predict.py"],
#         "data": BLD / "python" / "data" / "data_clean.csv",
#         "data_info": SRC / "data_management" / "data_info.yaml",
#     },
# )
# @pytask.mark.produces(BLD / "python" / "models" / "model.pickle")
# def task_fit_model_python(depends_on, produces):
#     """Fit a logistic regression model (Python version)."""
#     data_info = read_yaml(depends_on["data_info"])
#     data = pd.read_csv(depends_on["data"])
#     model = fit_logit_model(data, data_info, model_type="linear")
#     model.save(produces)


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
    def estimation_flir_constraint(depends_on, produces, basis):
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
    def estimation_flir_constraint(depends_on, produces, basis):
        consumption = pd.read_csv(depends_on["consumption"])
        LBMP = pd.read_csv(depends_on["LBMP"])
        wind = pd.read_csv(depends_on["wind"])
        result = flir(consumption, LBMP, wind, 11, basis, "harmonic")

        with open(produces, "wb") as f:
            pickle.dump(result, f, protocol=pickle.HIGHEST_PROTOCOL)


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
