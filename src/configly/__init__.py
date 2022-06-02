# flake8: noqa
from configly.config import Config
from configly.interpolators import EnvVarInterpolator, FileInterpolator, Interpolator
from configly.registry import register_interpolator, Registry

register_interpolator("ENV", EnvVarInterpolator)
register_interpolator("FILE", FileInterpolator)
