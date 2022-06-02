# flake8: noqa
from configly.config import Config
from configly.interpolators import EnvVarInterpolator, FileInterpolator, Interpolator
from configly.loaders import JsonLoader, TomlLoader, YamlLoader
from configly.registry import register_interpolator, Registry

register_interpolator("ENV", EnvVarInterpolator)
register_interpolator("FILE", FileInterpolator)

__all__ = [
    "Config",
    "EnvVarInterpolator",
    "FileInterpolator",
    "Interpolator",
    "JsonLoader",
    "Registry",
    "Registry",
    "TomlLoader",
    "YamlLoader",
    "register_interpolator",
]
