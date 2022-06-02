import os

from configly.interpolators import Interpolator
from configly.registry import registry


class DockerSecretInterpolator(Interpolator):
    def __getitem__(self, name):
        env_file = f"{name.upper()}_FILE"

        file_value = os.environ.get(env_file)
        if file_value is not None:
            # When the _FILE env var is set, the actual value is found by getting
            # the contents of the file at the location indicated by the env var.
            with open(file_value, "rb") as f:
                raw_value = f.read()

            value = raw_value.decode("utf-8")
            return value

        return os.environ[name]

    @classmethod
    def register(cls, registry=registry, overwrite=False):
        registry.register_interpolator("DOCKER_SECRET", cls, overwrite=overwrite)
