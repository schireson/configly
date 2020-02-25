import os

from configly.interpolators import Interpolator


class EnvVarInterpolator(Interpolator):
    def __getitem__(self, name):
        return os.environ[name]

    def get(self, name, default=None):
        return os.environ.get(name, default)
