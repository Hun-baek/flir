"""Tasks for managing the data."""

import pytask

from flir.config import BLD, SRC
from flir.data_management.clean_data import (
    clean_consumption,
    clean_LBMP,
    clean_source,
)
from flir.utilities import read_yaml


@pytask.mark.wip
@pytask.mark.depends_on({"data_info": SRC / "data_management" / "data_info.yaml"})
@pytask.mark.produces(
    {
        "consumption_cleaned": BLD / "data" / "consumption_cleaned.csv",
        "LBMP_cleaned": BLD / "data" / "LBMP_cleaned.csv",
        "source_cleaned": BLD / "data" / "wind_cleaned.csv",
    },
)
def task_clean_data(depends_on, produces):
    """Clean the consumption data."""
    data_info = read_yaml(depends_on["data_info"])

    consumption_path = SRC / "data" / "consumption"
    LBMP_path = SRC / "data" / "LBMP"
    source_path = SRC / "data" / "source"

    df_consumption = clean_consumption(consumption_path, data_info)
    df_LBMP = clean_LBMP(LBMP_path, data_info)
    df_wind = clean_source(source_path, data_info)

    df_consumption.to_csv(produces["consumption_cleaned"], index=False)
    df_LBMP.to_csv(produces["LBMP_cleaned"])
    df_wind.to_csv(produces["source_cleaned"])
