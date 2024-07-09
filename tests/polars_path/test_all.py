from pathlib import Path
import shutil

import polars as pl
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
