import functools
import os


class EnvVarInterpolator:
    yaml_safe = True

    def __getitem__(self, name):
        return os.environ[name]

    def get(self, name, default=None):
        return os.environ.get(name, default)


class FileInterpolator:
    yaml_safe = False

    @functools.lru_cache()
    def __getitem__(self, name):
        if not os.path.exists(name):
            raise KeyError("{} file does not exist.")

        with open(name, mode="rb") as f:
            return f.read().decode("utf-8")

    def get(self, name, default=None):
        try:
            return self[name]
        except KeyError:
            return default
