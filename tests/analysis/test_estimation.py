import pytest

import numpy as np
import pandas as pd

from flir.config import TEST_DIR
from flir.analysis.estimation import flir

DESIRED_NORM_VALUE = 10000


@pytest.fixture
def true_coef():
    num_obs_m = 100
    grid = np.linspace(0, 1, num=num_obs_m)

    varphi = (
        2 * np.sin(0.5 * np.pi * grid)
        + 4 * np.sin(1.5 * np.pi * grid)
        + 5 * np.sin(2.5 * np.pi * grid)
    )

    return varphi


@pytest.fixture
def response():
    return pd.read_csv(TEST_DIR / "analysis" / "response.csv")


@pytest.fixture
def regressor():
    return pd.read_csv(TEST_DIR / "analysis" / "regressor.csv")


@pytest.fixture
def instrument():
    return pd.read_csv(TEST_DIR / "analysis" / "instrument.csv")


def test_accuracy(true_coef, response, regressor, instrument):
    estimation_result = flir(
        response, regressor, instrument, 11, "fourier", "harmonic", logarithm=False
    )
    diff_vector = true_coef - estimation_result["varphi"]
    norm_diff = np.linalg.norm(diff_vector)
    assert norm_diff < DESIRED_NORM_VALUE
