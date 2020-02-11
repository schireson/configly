import os


class EnvVarInterpolator:
    def __getitem__(self, name):
        return os.environ[name]

    def get(self, name, default=None):
        return os.environ.get(name, default)
