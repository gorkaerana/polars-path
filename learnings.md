- Best to do follow [Rye's documentation](https://rye.astral.sh/guide/rust/#new-project) when developing with rye + maturin

- Python 3.8

- [Polars documentation](https://docs.pola.rs/user-guide/expressions/plugins/#setting-up) does not work straight up copy Cargo.toml from polars-hash

- Empty lib.rs

- Start from scratch with Polars documentation and using pip

- pyproject.toml like
```toml
[project]
name = "polars-plugin-extension-test"
version = "0.1.0"
description = "Add your description here"
authors = [
    { name = "Gorka Eraña", email = "eranagorka@gmail.com" }
]
dependencies = [
    "maturin",
    "polars",
]
readme = "README.md"
requires-python = ">= 3.8"

[build-system]
requires = ["maturin>=1.0,<2.0"]
build-backend = "maturin"
```

- https://stackoverflow.com/questions/71744403/pyo3-linker-error-when-using-extension-module-feature is solution to```
error: failed to select a version for `pyo3`.
    ... required by package `expression_lib v0.1.0 (/home/gorka/dev/polars_plugin_extension_test)`
versions that meet the requirements `*` are: 0.22.1, 0.22.0, 0.21.2, 0.21.1, 0.21.0, 0.20.3, 0.20.2, 0.20.1, 0.20.0, 0.19.2, 0.19.1, 0.19.0, 0.18.3, 0.18.2, 0.18.1, 0.18.0, 0.17.3, 0.17.2, 0.17.1, 0.17.0, 0.16.6, 0.16.5, 0.16.4, 0.16.3, 0.16.2, 0.16.1, 0.16.0, 0.15.2, 0.15.1, 0.15.0, 0.14.5, 0.14.4, 0.14.3, 0.14.2, 0.14.1, 0.14.0, 0.13.2, 0.13.1, 0.13.0, 0.12.4, 0.11.1, 0.11.0, 0.10.1, 0.9.2, 0.9.1, 0.9.0, 0.8.5, 0.8.4, 0.8.3, 0.8.2, 0.8.1, 0.8.0, 0.7.0, 0.6.0, 0.5.4, 0.5.3, 0.5.2, 0.5.0, 0.4.1, 0.4.0, 0.3.2, 0.3.1, 0.3.0, 0.2.7, 0.2.6, 0.2.5, 0.2.4, 0.2.3, 0.2.2, 0.2.1, 0.2.0, 0.1.0

the package `expression_lib` depends on `pyo3`, with features: `abi-py38` but `pyo3` does not have these features.


failed to select a version for `pyo3` which could resolve this conflict
💥 maturin failed
  Caused by: Cargo metadata failed. Does your crate compile with `cargo build`?
  Caused by: `cargo metadata` exited with an error:
  ```

- abi3-py38 instead of abi-py38

- added Jemalloc stuff copied from other plugin extensions

- maturin[patchelf]

- 
