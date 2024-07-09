import polars as pl

import polars_path as plp  # noqa  # type: ignore

if __name__ == "__main__":
    df = pl.DataFrame({"filepath": ["/etc/hosts", "kaka.jpeg"]})
    out = df.with_columns(pl.col("filepath").path.exists().alias("exists?"))
    print(out)
