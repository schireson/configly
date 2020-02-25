from types import MappingProxyType


class Registry:
    """A registry to allow for non-bundled interpolators and config loaders to be added.

    By default `Config` uses a global registry, to which you can `register_interpolator`.

    If you need more flexibility, you can pass `registry` to any of the `from_*` classmethods
    to use your own registry.

    >>> from configly import Config
    >>> local_registry = Registry()
    >>> config = Config.from_yaml('readthedocs.yml', registry=local_registry)
    """

    def __init__(self):
        self._interpolators = {}

    @property
    def interpolators(self):
        return MappingProxyType(self._interpolators)

    def clear_interpolators(self):
        self._interpolators.clear()

    def register_interpolator(self, name, interpolator_cls, overwrite=False):
        """Register a new interpolator for loading configuration from different sources.

        By default `Config` classes read from a global registry of interpolators. This function
        registers new interpolators to that global registry.

        For example, internally configly registers environment interpolation through a call like:

        >>> from configly import EnvVarInterpolator
        >>> register_interpolator("ENV", EnvVarInterpolator, overwrite=True)
        """
        if name in self._interpolators and not overwrite:
            raise ValueError("Name '{}' is already a registered interpolator".format(name))

        if isinstance(interpolator_cls, type):
            instance = interpolator_cls()
        else:
            instance = interpolator_cls

        self._interpolators[name] = instance


registry = Registry()
register_interpolator = registry.register_interpolator
