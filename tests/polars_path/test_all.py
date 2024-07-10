from pathlib import Path
import shutil

import polars as pl
from polars.datatypes import (
    Binary,
    Boolean,
    Date,
    Datetime,
    Duration,
    Float32,
    Float64,
    Int16,
    Int32,
    Int64,
    Int8,
    List,
    Null,
    Time,
    Unknown,
)
from polars.testing import assert_series_equal
import pytest

import polars_path as plp  # noqa


@pytest.fixture
def directory_hierarchy(tmp_path):
    (tmp_path / "exists.txt").touch()
    (tmp_path / "dir").touch()
    yield tmp_path
    shutil.rmtree(tmp_path)


@pytest.fixture
def filepaths(directory_hierarchy):
    return [
        str(directory_hierarchy / s)
        for s in ["exists.txt", "does_not_exist.txt", "dir"]
    ]


def test_exists(directory_hierarchy, filepaths):
    df = pl.DataFrame({"filepath": filepaths}).with_columns(
        exists=pl.col("filepath").path.exists()
    )
    assert_series_equal(df["exists"], pl.Series("exists", [True, False, True]))


def test_is_absolute(directory_hierarchy, filepaths):
    df = pl.DataFrame(
        {
            "filepath": [
                str(directory_hierarchy / s).lstrip(
                    str(list(directory_hierarchy.parents)[0])
                )
                if i > 0
                else str(directory_hierarchy / s)
                for i, s in enumerate(filepaths)
            ]
        }
    ).with_columns(is_absolute=pl.col("filepath").path.is_absolute())
    assert_series_equal(
        df["is_absolute"], pl.Series("is_absolute", [True, False, False])
    )


def test_is_file(directory_hierarchy, filepaths):
    df = pl.DataFrame({"filepath": filepaths}).with_columns(
        is_file=pl.col("filepath").path.is_file()
    )
    assert_series_equal(df["is_file"], pl.Series("is_file", [True, False, True]))


def test_parent(directory_hierarchy, filepaths):
    df = pl.DataFrame({"filepath": filepaths}).with_columns(
        parent=pl.col("filepath").path.parent()
    )
    assert_series_equal(
        df["parent"], pl.Series("parent", [str(Path(p).parent) for p in filepaths])
    )


def test_name(directory_hierarchy, filepaths):
    df = pl.DataFrame({"filepath": filepaths}).with_columns(
        name=pl.col("filepath").path.name()
    )
    assert_series_equal(
        df["name"], pl.Series("name", [str(Path(p).name) for p in filepaths])
    )


@pytest.mark.parametrize(
    "method_name", [m.method_name for m in plp.PATH_NAMESPACE_METHODS]
)
@pytest.mark.parametrize(
    "datatype",
    [
        Binary,
        Boolean,
        Date,
        Datetime,
        Duration,
        Float32,
        Float64,
        Int16,
        Int32,
        Int64,
        Int8,
        List,
        Null,
        Time,
        Unknown,
    ],
)
def test_compute_error_raised_with_non_string_data_type(method_name, datatype):
    with pytest.raises(pl.exceptions.ComputeError):
        pl.DataFrame({"filepath": [None, None]}).cast(datatype).with_columns(
            getattr(pl.col("filepath").path, method_name)().alias(method_name)
        )
    # TODO
    # assert f"'{method_name}' only works on string data, instead got" in str(exception_info.value)
