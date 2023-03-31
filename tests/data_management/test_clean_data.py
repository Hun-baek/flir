import pytest

from flir.config import TEST_DIR
from flir.data_management.clean_data import clean_consumption, clean_LBMP, clean_source
from flir.utilities import read_yaml


@pytest.fixture()
def consumption_path():
    return TEST_DIR / "data_management" / "consumption_mock"


@pytest.fixture()
def LBMP_path():
    return TEST_DIR / "data_management" / "LBMP_mock"


@pytest.fixture()
def wind_path():
    return TEST_DIR / "data_management" / "wind_mock"


@pytest.fixture()
def data_info():
    return read_yaml(TEST_DIR / "data_management" / "data_info_fixture.yaml")


def test_do_not_contain_summertimechangedays(
    consumption_path, LBMP_path, wind_path, data_info
):
    consumption_clean = clean_consumption(consumption_path, data_info)
    LBMP_clean = clean_LBMP(LBMP_path, data_info)
    source_clean = clean_source(wind_path, data_info)
    assert not set(data_info["summer_time_days"]).intersection(
        set(consumption_clean.T.columns)
    )
    assert not set(data_info["summer_time_days"]).intersection(
        set(LBMP_clean.T.columns)
    )
    assert not set(data_info["summer_time_days"]).intersection(
        set(source_clean.T.columns)
    )
