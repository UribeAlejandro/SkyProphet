from datetime import datetime

from pandas import DataFrame


def get_period_day(date: str) -> str:
    """
    Get the period of the day from a date
    Parameters
    ----------
    date : str
        Date in the format 'YYYY-MM-DD HH:MM:SS'
    Returns
    -------
    str
        Period of the day: 'mañana', 'tarde', 'noche'
    """
    date_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').time()
    morning_min = datetime.strptime("05:00", '%H:%M').time()
    morning_max = datetime.strptime("11:59", '%H:%M').time()
    afternoon_min = datetime.strptime("12:00", '%H:%M').time()
    afternoon_max = datetime.strptime("18:59", '%H:%M').time()
    evening_min = datetime.strptime("19:00", '%H:%M').time()
    evening_max = datetime.strptime("23:59", '%H:%M').time()
    night_min = datetime.strptime("00:00", '%H:%M').time()
    night_max = datetime.strptime("4:59", '%H:%M').time()

    if (date_time > morning_min and date_time < morning_max):
        return 'mañana'
    elif (date_time > afternoon_min and date_time < afternoon_max):
        return 'tarde'
    elif (
            (date_time > evening_min and date_time < evening_max) or
            (date_time > night_min and date_time < night_max)
    ):
        return 'noche'


def is_high_season(fecha: str) -> int:
    """
    Check if a date is in high season
    Parameters
    ----------
    fecha : str
        Date in the format 'YYYY-MM-DD HH:MM:SS'
    Returns
    -------
    int
        1 if the date is in high season, 0 otherwise
    """
    fecha_anio = int(fecha.split('-')[0])
    fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
    range1_min = datetime.strptime('15-Dec', '%d-%b').replace(year=fecha_anio)
    range1_max = datetime.strptime('31-Dec', '%d-%b').replace(year=fecha_anio)
    range2_min = datetime.strptime('1-Jan', '%d-%b').replace(year=fecha_anio)
    range2_max = datetime.strptime('3-Mar', '%d-%b').replace(year=fecha_anio)
    range3_min = datetime.strptime('15-Jul', '%d-%b').replace(year=fecha_anio)
    range3_max = datetime.strptime('31-Jul', '%d-%b').replace(year=fecha_anio)
    range4_min = datetime.strptime('11-Sep', '%d-%b').replace(year=fecha_anio)
    range4_max = datetime.strptime('30-Sep', '%d-%b').replace(year=fecha_anio)

    if ((fecha >= range1_min and fecha <= range1_max) or
            (fecha >= range2_min and fecha <= range2_max) or
            (fecha >= range3_min and fecha <= range3_max) or
            (fecha >= range4_min and fecha <= range4_max)):
        return 1
    else:
        return 0


def get_min_diff(data: DataFrame, initial_date_col: str = 'Fecha-O', final_date_col: str = 'Fecha-I') -> float:
    """
    Get the difference in minutes between two dates
    Parameters
    ----------
    data : DataFrame
        DataFrame with the columns 'Fecha-O' and 'Fecha-I'
    initial_date_col : str
        Column name of the initial date
    final_date_col : str
        Column name of the final date

    Returns
    -------
    float
        Difference in minutes between final and initial date
    """
    fecha_o = datetime.strptime(data[initial_date_col], '%Y-%m-%d %H:%M:%S')
    fecha_i = datetime.strptime(data[final_date_col], '%Y-%m-%d %H:%M:%S')
    min_diff = ((fecha_o - fecha_i).total_seconds())/60
    return min_diff


def get_rate_from_column(data: DataFrame, column: str) -> DataFrame:
    """
    Get the rate of delays for each category in a column
    Parameters
    ----------
    data : DataFrame
        A DataFrame with the column 'delay'
    column : str
        Column to calculate the rate

    Returns
    -------
    DataFrame
        A DataFrame with the rate of delays for each category in the column
    """

    delays = {}
    for _, row in data.iterrows():
        if row['delay'] == 1:
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

    return DataFrame.from_dict(data=rates, orient='index', columns=['Tasa (%)'])
