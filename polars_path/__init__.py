from pathlib import Path

import polars as pl
from polars.plugins import register_plugin_function


@pl.api.register_expr_namespace("path")
class PathNamespace:
    def __init__(self, expr: pl.Expr):
        self._expr = expr

    def exists(self) -> pl.Expr:
        """Equivalent to https://docs.python.org/3/library/os.path.html#os.path.exists and https://docs.python.org/3/library/pathlib.html#pathlib.Path.exists. Implemented via https://doc.rust-lang.org/std/path/struct.Path.html#method.exists"""
        return register_plugin_function(
            plugin_path=Path(__file__).parent,
            function_name="exists",
            args=self._expr,
            is_elementwise=True,
        )

    def is_absolute(self) -> pl.Expr:
        """Equivalent to https://docs.python.org/3/library/os.path.html#os.path.isabs and https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.is_absolute. Implemented with https://doc.rust-lang.org/std/path/struct.Path.html#method.is_absolute"""
        return register_plugin_function(
            plugin_path=Path(__file__).parent,
            function_name="is_absolute",
            args=self._expr,
            is_elementwise=True,
        )

    def is_file(self) -> pl.Expr:
        """Equivalent to https://docs.python.org/3/library/os.path.html#os.path.isfile and https://docs.python.org/3/library/pathlib.html#pathlib.Path.is_file. Implemented with https://doc.rust-lang.org/std/path/struct.Path.html#method.is_file"""
        return register_plugin_function(
            plugin_path=Path(__file__).parent,
            function_name="is_file",
            args=self._expr,
            is_elementwise=True,
        )

    def is_dir(self) -> pl.Expr:
        """Equivalent to https://docs.python.org/3/library/os.path.html#os.path.isdir and https://docs.python.org/3/library/pathlib.html#pathlib.Path.is_dir. Implemented with https://doc.rust-lang.org/std/path/struct.Path.html#method.is_dir"""
        return register_plugin_function(
            plugin_path=Path(__file__).parent,
            function_name="is_dir",
            args=self._expr,
            is_elementwise=True,
        )

    def parent(self) -> pl.Expr:
        """Equivalent to https://docs.python.org/3/library/os.path.html#os.path.dirname and https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.parent. Implemented with https://doc.rust-lang.org/std/path/struct.Path.html#method.parent"""
        return register_plugin_function(
            plugin_path=Path(__file__).parent,
            function_name="parent",
            args=self._expr,
            is_elementwise=True,
        )
