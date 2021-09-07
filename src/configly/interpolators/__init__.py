import abc


class Interpolator(abc.ABC):
    """ABC to define the interface required by an interpolator.

    It is not required to subclass `Interpolator`, but it *does* provide the interface
    and ensures the class implements it.
    """

    @abc.abstractmethod
    def __getitem__(self, name):
        """Override this method to implement a method to get the value for a piece of config.

        This method should return a `KeyError` when the value cannot be found.
        """

    def get(self, name, default=None):
        """Implement get operation with a default.

        Override this method to get more tailored behavior.
        """
        try:
            return self[name]
        except KeyError:
            return default


from configly.interpolators.env import EnvVarInterpolator  # noqa, isort:skip
from configly.interpolators.file import FileInterpolator  # noqa, isort:skip
