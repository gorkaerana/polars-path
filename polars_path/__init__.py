from pathlib import Path  # noqa

import polars as pl
from polars.plugins import register_plugin_function  # noqa


@pl.api.register_expr_namespace("path")
class PathNamespace:
    def __init__(self, expr: pl.Expr):
        self._expr = expr


class PathNamespaceMethod:
    os_path_link_prefix = "https://docs.python.org/3/library/os.path.html#os.path."
    pathlib_link_prefix = (
        "https://docs.python.org/3/library/pathlib.html#pathlib.PurePath."
    )
    std_path_link_prefix = "https://doc.rust-lang.org/std/path/struct.Path.html#method."

    def __init__(
        self,
        os_path_link_suffix: str,
        pathlib_link_suffix: str,
        std_path_link_suffix: str,
        method_name: str,
    ):
        self.os_path_link_suffix = os_path_link_suffix
        self.pathlib_link_suffix = pathlib_link_suffix
        self.std_path_link_suffix = std_path_link_suffix
        self.method_name = method_name

    def __repr__(self):
        attributes = [
            "os_path_link_suffix",
            "pathlib_link_suffix",
            "std_path_link_suffix",
            "method_name",
        ]
        pretty_attrs = ", ".join(f"{a}={repr(getattr(self, a))}" for a in attributes)
        return f"{self.__class__.__name__}({pretty_attrs})"

    @property
    def docstring(self):
        return (
            f"Equivalent to {self.os_path_link_prefix}{self.os_path_link_suffix}, "
            f"and {self.pathlib_link_prefix}{self.pathlib_link_suffix}. Implemented "
            f"with {self.std_path_link_prefix}{self.std_path_link_suffix}"
        )

    @property
    def method_lines(self):
        return [
            f"def {self.method_name}(self) -> pl.Expr:",
            "    return register_plugin_function(",
            "        plugin_path=Path(__file__).parent,",
            f'        function_name="{self.method_name}",',
            "        args=self._expr,",
            "        is_elementwise=True",
            "    )",
        ]

    def make(self):
        exec("\n".join(self.method_lines), globals())
        exec(
            f'{self.method_name}.__docstring__ = "{self.docstring}"',
            globals(),
        )
        setattr(PathNamespace, self.method_name, globals()[self.method_name])


PATH_NAMESPACE_METHODS: tuple[PathNamespaceMethod, ...] = (
    PathNamespaceMethod("exists", "exists", "exists", "exists"),
    PathNamespaceMethod("isabs", "is_absolute", "is_absolute", "is_absolute"),
    PathNamespaceMethod("isfile", "is_file", "is_file", "is_file"),
    PathNamespaceMethod("isdir", "is_dir", "is_dir", "is_dir"),
    PathNamespaceMethod("dirname", "parent", "parent", "parent"),
)

for method in PATH_NAMESPACE_METHODS:
    method.make()
