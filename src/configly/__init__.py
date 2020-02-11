# flake8: noqa
def get_package_name():
    return __name__.split(".")[0]


from configly.config import Config
from configly.interpolators import EnvVarInterpolator, FileInterpolator
from configly.registry import register_interpolator

register_interpolator("ENV", EnvVarInterpolator)
register_interpolator("FILE", FileInterpolator)
