"""Functions for fitting the regression model."""


import numpy as np
import pandas as pd
import skfda
import math

from skfda.representation.basis import BSpline, Fourier
from skfda.misc import inner_product
from skfda.representation.grid import FDataGrid
from skfda.preprocessing.smoothing import BasisSmoother


def flir(consumption, LBMP, wind, n_basis, basis, constraint):
    """Estimate volatile price elasticity in energy market.

    Args:
    - consumption: Pandas DataFrame of consumption data
    - LBMP: Pandas DataFrame of LBMP data
    - wind: Pandas DataFrame of wind generation data
    - n_basis: int, number of basis functions
    - basis: str, choose either "bspline" or "fourier" basis functions
    - constraint: boolean, use constraint or not

    Returns:
    - varphi: array of estimated coefficient function
    - df: Pandas DataFrame of values of GCV and its corresponding regularization value
    - min_xi: int of regularization value holding the minimum GCV value

    """

    # Extract sample sizes
    num_sample = consumption.shape[0]

    if LBMP.shape[0] == num_sample and wind.shape[0] == num_sample:
        n = consumption.shape[0]
    else:
        raise ValueError("All variables should have the same sample size")

    # Grids
    hours = np.arange(0, 24)
    grid = np.linspace(0, 23, 101)

    # Remove the first columns and use logarithm
    consumption = np.log10(consumption.iloc[:, 1:])
    LBMP = np.log10(LBMP.iloc[:, 1:])
    wind = np.log10(wind.iloc[:, 1:])

    # Rename
    LBMP.columns = hours
    wind.columns = hours

    # Remove NA values of wind
    if wind.isnull().values.any():

        idx = wind.dropna().index

        consumption = consumption.loc[idx, :]
        LBMP = LBMP.loc[idx, :]
        wind = wind.loc[idx, :]

    cnum_sample = consumption.shape[0]

    # Convert the data to functional data type
    f_LBMP = skfda.FDataGrid(data_matrix=LBMP, grid_points=hours)
    f_wind = skfda.FDataGrid(data_matrix=wind, grid_points=hours)

    # Create basis functions that will be used to expand functional data
    if basis == "bspline":
        basis_obj = BSpline(n_basis=n_basis, domain_range=(0, 23), order=4)
    elif basis == "fourier":
        basis_obj = Fourier(n_basis=n_basis, domain_range=(0, 23))

    mat_basis = basis_obj(hours).T
    mat_basis2 = basis_obj(grid).T
    mat_basis2 = np.squeeze(mat_basis2)

    lbmp_coef = f_LBMP.to_basis(basis_obj).coefficients
    wind_coef = f_wind.to_basis(basis_obj).coefficients

    # Create Penalty matrix
    if constraint == "second_derivative":
        penalty = inner_product(
            basis_obj.derivative(order=2), basis_obj.derivative(order=2), _matrix=True
        )

    elif constraint == "harmonic":
        a_part = inner_product(
            (2 * math.pi / 24) ** 2 * basis_obj.derivative(order=1),
            (2 * math.pi / 24) ** 2 * basis_obj.derivative(order=1),
            _matrix=True,
        )
        b_part = inner_product(
            basis_obj.derivative(order=3),
            (2 * math.pi / 24) ** 2 * basis_obj.derivative(order=1),
            _matrix=True,
        )
        c_part = inner_product(
            basis_obj.derivative(order=3), basis_obj.derivative(order=3), _matrix=True
        )
        penalty = a_part + 2 * b_part + c_part
    else:
        penalty = inner_product(basis_obj, basis_obj, _matrix=True)

    new_penalty = np.vstack((np.zeros((1, n_basis)), penalty))
    new_penalty = np.hstack((np.zeros((n_basis + 1, 1)), new_penalty))

    # Innter product of basis function
    Q = inner_product(basis_obj, basis_obj, _matrix=True)

    P = np.dot(lbmp_coef, Q)
    P = np.hstack((np.ones((cnum_sample, 1)), P))

    J = np.dot(mat_basis, np.dot(wind_coef.T, P))
    J = np.squeeze(J)
    I = np.eye(24)

    r = np.dot(wind.T, consumption["MWh"]) / n
    r_exp = BasisSmoother(basis_obj).fit_transform(FDataGrid(r, hours))
    r_smt = r_exp.data_matrix

    log_xi_vec = np.arange(-8, 3, 0.0025)
    n_xi = len(log_xi_vec)
    r_smt = np.squeeze(r_smt)

    log_xi_vec = np.arange(-8, 3.0025, 0.0025)
    n_xi = len(log_xi_vec)

    gcv_vec = []

    # Execute GCV to decide the regularization parameter, xi
    for i in range(n_xi):
        xi = 10 ** log_xi_vec[i]

        hat_mat = (
            (1 / (n**2))
            * J
            @ np.linalg.inv((1 / (n**2)) * J.T @ J + xi * new_penalty)
            @ J.T
        )

        tr_hatmat = np.trace(I - hat_mat)

        sse = np.sum((r_smt - hat_mat @ r_smt) ** 2)

        gcv = (1 / n * sse) / ((1 / n * tr_hatmat) ** 2)

        gcv_vec.append(gcv)

    df = pd.DataFrame({"gcv": gcv_vec, "log_xi": log_xi_vec})

    log_min_xi = df.loc[df["gcv"].idxmin(), "log_xi"]

    # Derive the estimated coefficient matrix
    bundle_mat = np.linalg.inv(
        1 / (n**2) * J.T @ J + 10**log_min_xi * new_penalty
    ) @ (1 / n * J.T @ r_smt)

    # Estimated coefficient function
    varphi = mat_basis2 @ bundle_mat[1:]

    return {"varphi": varphi, "df": df}
