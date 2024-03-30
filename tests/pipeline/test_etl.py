import os

from challenge.pipeline.etl import etl_pipeline, extract_data, load_data
from tests.constants import path_data


def test_extract():
    df = extract_data(path_data)
    assert len(df) > 0


def test_load_data():
    output_path = "data/test/data.csv"
    df = extract_data(path_data)
    load_data(df, output_path)

    assert os.path.isfile(output_path)


def test_etl_pipeline():
    df = extract_data(path_data)
    features, target = etl_pipeline(df)

    assert len(df) == len(target)
    assert len(df) == len(features)
    assert len(df.columns) > len(list(target.columns))
    assert len(df.columns) < len(list(features.columns))
