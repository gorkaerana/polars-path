from pathlib import Path

import polars as pl
from polars.plugins import register_plugin_function


@pl.api.register_expr_namespace("path")
class PathNamespace:
    def __init__(self, expr: pl.Expr):
        self._expr = expr

    def exists(self) -> pl.Expr:
        """Pig-latinnify expression."""
        return register_plugin_function(
            plugin_path=Path(__file__).parent,
            function_name="exists",
            args=self._expr,
            is_elementwise=True,
        )
