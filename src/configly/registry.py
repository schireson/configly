from types import MappingProxyType


class Registry:
    def __init__(self):
        self._interpolators = {}

    @property
    def interpolators(self):
        return MappingProxyType(self._interpolators)

    def clear_interpolators(self):
        self._interpolators.clear()

    def register_interpolator(self, name, interpolator_cls, overwrite=False):
        if name in self._interpolators and not overwrite:
            raise ValueError("Name '{}' is already a registered interpolator".format(name))

        if isinstance(interpolator_cls, type):
            instance = interpolator_cls()
        else:
            instance = interpolator_cls

        self._interpolators[name] = instance


registry = Registry()
register_interpolator = registry.register_interpolator
