from datetime import datetime
from typing import Optional, Tuple

import numpy as np
import pandas as pd

from challenge.constants import DUMMY_COLUMNS, THRESHOLD_IN_MINUTES


def get_period_day(date):
    date_time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").time()
    morning_min = datetime.strptime("05:00", "%H:%M").time()
    morning_max = datetime.strptime("11:59", "%H:%M").time()
    afternoon_min = datetime.strptime("12:00", "%H:%M").time()
    afternoon_max = datetime.strptime("18:59", "%H:%M").time()
    evening_min = datetime.strptime("19:00", "%H:%M").time()
    evening_max = datetime.strptime("23:59", "%H:%M").time()
    night_min = datetime.strptime("00:00", "%H:%M").time()
    night_max = datetime.strptime("4:59", "%H:%M").time()

    if date_time > morning_min and date_time < morning_max:
        return "mañana"
    elif date_time > afternoon_min and date_time < afternoon_max:
        return "tarde"
    elif (date_time > evening_min and date_time < evening_max) or (date_time > night_min and date_time < night_max):
        return "noche"


def is_high_season(fecha: str) -> int:
    """Check if the date is in high season.

    Parameters
    ----------
    fecha : str
        Date in format "YYYY-MM-DD HH:MM:SS".
    Returns
    -------
    int
        1 if the date is in high season, 0 otherwise.
    """
    fecha_anio = int(fecha.split("-")[0])
    fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
    range1_min = datetime.strptime("15-Dec", "%d-%b").replace(year=fecha_anio)
    range1_max = datetime.strptime("31-Dec", "%d-%b").replace(year=fecha_anio)
    range2_min = datetime.strptime("1-Jan", "%d-%b").replace(year=fecha_anio)
    range2_max = datetime.strptime("3-Mar", "%d-%b").replace(year=fecha_anio)
    range3_min = datetime.strptime("15-Jul", "%d-%b").replace(year=fecha_anio)
    range3_max = datetime.strptime("31-Jul", "%d-%b").replace(year=fecha_anio)
    range4_min = datetime.strptime("11-Sep", "%d-%b").replace(year=fecha_anio)
    range4_max = datetime.strptime("30-Sep", "%d-%b").replace(year=fecha_anio)

    if (
        (fecha >= range1_min and fecha <= range1_max)
        or (fecha >= range2_min and fecha <= range2_max)
        or (fecha >= range3_min and fecha <= range3_max)
        or (fecha >= range4_min and fecha <= range4_max)
    ):
        return 1
    else:
        return 0


def get_min_diff(data: pd.DataFrame) -> float:
    """Get the difference in minutes between two dates.

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe with columns "Fecha-O" and "Fecha-I".
    Returns
    -------
    float
        Difference in minutes.
    """
    fecha_o = datetime.strptime(data["Fecha-O"], "%Y-%m-%d %H:%M:%S")
    fecha_i = datetime.strptime(data["Fecha-I"], "%Y-%m-%d %H:%M:%S")
    min_diff = ((fecha_o - fecha_i).total_seconds()) / 60
    return min_diff


def get_rate_from_column(data: pd.DataFrame, column: str) -> pd.DataFrame:
    """Get the rate of delays for each category in a column.

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe with the raw data.
    column: str
        Column name.
    Returns
    -------
    pd.DataFrame
        Dataframe with the rate of delays for each category.
    """
    delays = {}
    for _, row in data.iterrows():
        if row["delay"] == 1:
            if row[column] not in delays:
                delays[row[column]] = 1
            else:
                delays[row[column]] += 1
    total = data[column].value_counts().to_dict()

    rates = {}
    for name, total in total.items():
        if name in delays:
            rates[name] = round(total / delays[name], 2)
        else:
            rates[name] = 0

    return pd.DataFrame.from_dict(data=rates, orient="index", columns=["Tasa (%)"])


def calculate_target(data: pd.DataFrame, target_column: str) -> pd.DataFrame:
    """Calculate the target column based on the threshold.

    Parameters
    ----------
    data : pd.DataFrame
        Raw data.
    target_column : str
        Target column name.
    Returns
    -------
    pd.Series
        Target column.
    """
    data[target_column] = np.where(data["min_diff"] > THRESHOLD_IN_MINUTES, 1, 0)
    target = data[target_column]
    target = target.to_frame()
    return target


def transform_categorical(data: pd.DataFrame) -> pd.DataFrame:
    """Transform categorical columns into dummy variables.

    Parameters
    ----------
    data : pd.DataFrame
        Raw data.

    Returns
    -------
    pd.DataFrame
        Transformed data.
    """
    dummies = [pd.get_dummies(data[dummy_col], prefix=dummy_col) for dummy_col in DUMMY_COLUMNS]
    features = pd.concat(dummies, axis=1)
    return features


def etl_pipeline(data: pd.DataFrame, target_column: Optional[str] = "delay") -> Tuple[pd.DataFrame, pd.Series]:
    """Execute the ETL pipeline.

    Parameters
    ----------
    data : pd.DataFrame
        Raw data.
    target_column : str, optional
        Target column name.
    Returns
    -------
    pd.DataFrame
        Features.
    pd.Series
        Target.
    """
    data["min_diff"] = data.apply(get_min_diff, axis=1)
    features, target = transform_data(data, target_column)
    return features, target


def extract_data(data_path: str) -> pd.DataFrame:
    """Extract data from a CSV file.

    Parameters
    ----------
    data_path : str
        Path to the CSV file.
    Returns
    -------
    pd.DataFrame
        Raw data.
    """
    data = pd.read_csv(data_path)
    return data


def transform_data(data: pd.DataFrame, target_column: str) -> Tuple[pd.DataFrame, pd.Series]:
    """Transform the raw data.

    Parameters
    ----------
    data : pd.DataFrame
        Raw data.
    target_column : str
        Target column name.
    Returns
    -------
    Tuple[pd.DataFrame, pd.Series]
        Features and target.
    """
    features = transform_categorical(data)
    target = calculate_target(data, target_column)
    return features, target


def load_data(data: pd.DataFrame, output_path: str) -> None:
    """Load the transformed data.

    Parameters
    ----------
    data : pd.DataFrame
        Features.
    output_path : str
        Path to save the data.
    """
    data.to_csv(output_path, index=False)
