"""Functions plotting results."""

import plotly.express as px
import matplotlib.pyplot as plt
import seaborn


def plot_estimated_function(data, basis_type):
    """Plot of estimated regression function.

    Parameters
    ----------
    data : pandas.DataFrame
        merged data frame of estimated regression function
    basis_type : str
        either fourier or bspline

    Returns
    -------
    fig : plotly.graph_objects.Figure: The figure

    """

    fig = px.line(
        data,
        x="grid",
        y=[f"{basis_type}", f"{basis_type}_constraint", f"{basis_type}_harmonic"],
        labels={"grid": "Hours", "value": r"$\hat{\varphi}$"},
        width=1200,
    )

    new_names = ["None", r"$D^2$", r"$H$"]

    for i, new_name in enumerate(new_names):
        fig.data[i].name = new_name

    fig.update_xaxes(dtick=1)

    fig.update_layout(
        legend=dict(
            orientation="h",
            entrywidth=100,
            yanchor="top",
            y=-0.3,
            xanchor="center",
            x=0.7,
            title="",
        )
    )

    return fig


def plot_hourly(data, value_name, produces):
    """Plot of hourly recorded generation and LBMP.

    Parameters
    ----------
    data : pandas DataFrame
        LBMP data or electricity generation data
    value_name : str
        either Generation or LBMP
    produces: str
        path for save

    Returns
    -------

    """

    data = data.drop("Date", axis=1)
    data.dropna(inplace=True)
    data = data.T
    data.reset_index(drop=False, inplace=True)
    data["index"] = list(range(24))
    data.rename(columns={"index": "Hour"}, inplace=True)

    data = data.melt(id_vars=["Hour"], value_name=value_name)

    fig, ax = plt.subplots(figsize=(8, 5))
    seaborn.boxplot(x=data["Hour"], y=data[value_name], showfliers=False, ax=ax)

    plt.savefig(produces)
