import functools
import os

from configly.interpolators import Interpolator


class FileInterpolator(Interpolator):
    yaml_safe = False

    @functools.lru_cache()
    def __getitem__(self, name):
        if not os.path.exists(name):
            raise KeyError("{} file does not exist.")

        with open(name, mode="rb") as f:
            return f.read().decode("utf-8")
