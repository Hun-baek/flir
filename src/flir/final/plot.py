"""Functions plotting results."""

import plotly.express as px


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
