"""Function(s) for cleaning the data set(s)."""

import os

import pandas as pd


def clean_consumption(consumption_path, data_info):
    """This function returns the cleaned consumption data set.

    Parameters
    ----------
    LBMP_path : Path to consumption data
    data_info : data information for cleaning

    Returns:
    -------
    df : pandas.DataFrame
        The cleaned data consumption set

    """
    csv_list = os.listdir(consumption_path)

    df = pd.DataFrame()

    for csv in csv_list:

        data = pd.read_csv(consumption_path / csv)
        data = data.drop(data.columns[0], axis=1)
        data = data.dropna(axis=0)
        data.columns = ["Date", "MWh"]

        df = pd.concat([df, data])

    dates = df["Date"].str.split(",")

    df["Date"] = dates.str.get(0)
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")

    day_week = [0, 1, 2, 3, 4]
    df = df[df["Date"].dt.dayofweek.isin(day_week)]

    summer_time_days = data_info["summer_time_days"]
    df = df[~df["Date"].isin(summer_time_days)]

    return df


def clean_LBMP(LBMP_path, data_info):
    """This function returns the cleaned LBMP data set.

    Parameters
    ----------
    LBMP_path : Path to LBMP data
    data_info : data information for cleaning

    Returns:
    -------
    df : pandas.DataFrame
        The cleaned LBMP data

    """
    csv_list = os.listdir(LBMP_path)

    df = pd.DataFrame()

    for csv in csv_list:

        data = pd.read_csv(LBMP_path / csv)

        data = data[data_info["LBMP_columns"]]
        date_time = data["Eastern Date Hour"].str.split(" ")

        data["Date"] = date_time.str.get(0)
        data["Time"] = date_time.str.get(1)

        data["Date"] = pd.to_datetime(data["Date"], format="%Y/%m/%d")
        data["Date"] = data["Date"].dt.strftime("%m/%d/%Y")
        data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")

        day_week = [0, 1, 2, 3, 4]
        data = data[data["Date"].dt.dayofweek.isin(day_week)]

        summer_time_days = data_info["summer_time_days"]
        data = data[~data["Date"].isin(summer_time_days)]

        data.reset_index(inplace=True, drop=True)
        data = data.groupby(["Date", "Time"], as_index=False).mean(numeric_only=True)

        a = data.groupby(["Date", "Time"]).sum()

        data = a.unstack()
        data = data.droplevel(level=0, axis=1)

        df = pd.concat([df, data])

    return df


def clean_source(source_path, data_info):
    """This function cleans wind generation data.

    Parameters
    ----------
    source_path : Path to wind generation data
    data_info : data information for cleaning

    Returns:
    -------
    df : pandas.DataFrame
        The cleaned wind generation data

    """
    csv_list = os.listdir(source_path)

    if "desktop.ini" in csv_list:
        csv_list.remove("desktop.ini")

    df = pd.DataFrame()

    for csv in csv_list:

        data = pd.read_csv(source_path / csv)

        if data.columns[3] == "Gen MW":
            data.rename(columns={"Gen MW": "Gen MWh"}, inplace=True)

        data = data[data["Fuel Category"].isin(["Wind", "Hydro"])]
        data = data.drop(["Time Zone"], axis=1)

        data["Time Stamp"] = pd.to_datetime(data["Time Stamp"]).dt.strftime(
            "%m/%d/%Y %H",
        )
        data = data.groupby(["Time Stamp"], as_index=False).sum(numeric_only=True)

        df = pd.concat([df, data])

    df.columns = ["Date", "MWh"]
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y %H")
    df["Date"] = df["Date"].dt.strftime("%m/%d/%Y %H:%M:%S")

    date_time = df["Date"].str.split(" ")

    df["Time"] = date_time.str.get(1)

    df["Date"] = date_time.str.get(0)
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")

    day_week = [0, 1, 2, 3, 4]
    df = df[df["Date"].dt.dayofweek.isin(day_week)]

    summer_time_days = data_info["summer_time_days"]
    df = df[~df["Date"].isin(summer_time_days)]

    df.reset_index(inplace=True, drop=True)

    a = df.groupby(["Date", "Time"]).sum()

    df = a.unstack()
    df = df.droplevel(level=0, axis=1)

    return df
