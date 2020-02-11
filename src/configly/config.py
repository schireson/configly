import copy
from collections.abc import Mapping

from configly.loaders import JsonLoader, TomlLoader, YamlLoader
from configly.process import post_process
from configly.registry import registry


class Config:
    def __init__(self, value=None, _src_input=None, _loader=None, _registry=registry):
        if value is None:
            value = {}
        self._value = value

        self._src_input = _src_input
        self._loader = _loader
        self._registry = _registry

    @classmethod
    def from_loader(cls, loader, file, registry=registry):
        with open(file, "rb") as f:
            result = loader.load(f)

        output = post_process(loader=loader, value=result, registry=registry)
        return cls(output, _src_input=result, _loader=loader, _registry=registry)

    @classmethod
    def from_yaml(cls, file, registry=registry):
        """Open a yaml `file` and load it into the resulting config object.
        """
        return cls.from_loader(YamlLoader(), file, registry=registry)

    @classmethod
    def from_json(cls, file, registry=registry):
        """Open a toml `file` and load it into the resulting config object.
        """
        return cls.from_loader(JsonLoader(), file, registry=registry)

    @classmethod
    def from_toml(cls, file, registry=registry):
        """Open a toml `file` and load it into the resulting config object.
        """
        return cls.from_loader(TomlLoader(), file, registry=registry)

    def refresh(self):
        update = post_process(loader=self._loader, value=self._src_input, registry=self._registry)
        self._value.update(update)

    def to_dict(self):
        return copy.deepcopy(self._value)

    def __iter__(self):
        for key, value in self._value.items():
            if isinstance(value, Mapping):
                value = self.__class__(
                    value,
                    _src_input=self._src_input and self._src_input[key],
                    _loader=self._loader,
                    _registry=self._registry,
                )

            yield key, value

    def __getitem__(self, attr):
        try:
            value = self._value[attr]
        except KeyError:
            raise KeyError("'{}' not found in: {}.".format(attr, self))

        if isinstance(value, Mapping):
            return self.__class__(
                value,
                _src_input=self._src_input and self._src_input[attr],
                _loader=self._loader,
                _registry=self._registry,
            )
        return value

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            if hasattr(self._value, name):
                return getattr(self._value, name)
            raise AttributeError(str(e))

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self._value == other._value
        return self._value == other

    def __repr__(self):
        return "{0.__class__.__name__}({0._value})".format(self)
