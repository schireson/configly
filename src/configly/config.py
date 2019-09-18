import copy
import re
from collections.abc import Iterable, Mapping

from configly.interpolators import EnvVarInterpolator, FileInterpolator
from configly.loaders import JsonLoader, TomlLoader, YamlLoader

default_interpolation_types = {"ENV": EnvVarInterpolator(), "FILE": FileInterpolator()}


def post_process(loader, value, interpolation_types=None):
    if isinstance(value, Mapping):
        result = {}
        for key, item in value.items():
            result[key] = post_process(loader, item, interpolation_types=interpolation_types)
        return result

    elif isinstance(value, Iterable) and not isinstance(value, str):
        result = []
        for item in value:
            result.append(post_process(loader, item, interpolation_types=interpolation_types))
        return result

    else:
        if not isinstance(value, str):
            return value

        match = re.match(r"(.*)\<%\s*(\w+)\[([\w.]+)(?:,\s*(.+))?\]\s*%>(.*)", value)
        if match:
            groups = match.groups()
            pre, interpolation_type, var_name, default, post = groups

            all_interpolation_types = {**default_interpolation_types, **(interpolation_types or {})}
            if interpolation_type not in all_interpolation_types:
                raise ValueError("Unrecognized loader type: {}".format(interpolation_type))

            interpolator = all_interpolation_types[interpolation_type]
            if default is None:
                try:
                    var_value = interpolator[var_name]
                except KeyError:
                    raise ValueError(
                        "The requested {} value '{}' was not found".format(
                            interpolation_type.lower(), var_name
                        )
                    )
            else:
                var_value = interpolator.get(var_name, default)

            result = pre + var_value + post

            if getattr(interpolator, "yaml_safe", True):
                return loader.load_value(result)
            return result
        return value


class Config:
    def __init__(self, value=None):
        if value is None:
            value = {}
        self._value = value

    @classmethod
    def from_loader(cls, loader, file, interpolation_types=None):
        with open(file, "rb") as f:
            result = loader.load(f)

        return cls(post_process(loader, result, interpolation_types=interpolation_types))

    @classmethod
    def from_yaml(cls, file, interpolation_types=None):
        """Open a yaml `file` and load it into the resulting config object.
        """
        return cls.from_loader(YamlLoader(), file, interpolation_types)

    @classmethod
    def from_json(cls, file, interpolation_types=None):
        """Open a toml `file` and load it into the resulting config object.
        """
        return cls.from_loader(JsonLoader(), file, interpolation_types)

    @classmethod
    def from_toml(cls, file, interpolation_types=None):
        """Open a toml `file` and load it into the resulting config object.
        """
        return cls.from_loader(TomlLoader(), file, interpolation_types)

    def to_dict(self):
        return copy.deepcopy(self._value)

    def __iter__(self):
        for key, value in self._value.items():
            if isinstance(value, Mapping):
                value = self.__class__(value)

            yield key, value

    def __getitem__(self, attr):
        try:
            value = self._value[attr]
        except KeyError:
            raise KeyError("'{}' not found in: {}.".format(attr, self))

        if isinstance(value, Mapping):
            return self.__class__(value)
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
