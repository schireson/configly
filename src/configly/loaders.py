import importlib
import json
from typing import TypeVar


class YamlLoader:
    def __init__(self):
        try:
            from ruamel.yaml import YAML
        except ImportError:
            raise ImportError("Install `configly[yaml]` to use the yaml loader.")

        yaml = YAML(typ="safe")

        self.decoder = yaml

    def load(self, value):
        return self.decoder.load(value)

    def loads(self, value):
        return self.load(value)

    def load_value(self, value):
        return self.decoder.load(value)


class JsonLoader:
    def __init__(self):
        self.decoder = json.JSONDecoder()

    def load(self, value):
        return json.load(value)

    def loads(self, value: str):
        return json.loads(value)

    def load_value(self, value):
        try:
            return self.decoder.decode(value)
        except ValueError:
            return value


def _tomli_parse_value(loader, value):
    return loader._parser.parse_value(value, 0, float)[1]


def _toml_parse_value(loader, value):
    decoder = loader.TomlDecoder()
    return decoder.load_value(value)[0]


class TomlLoader:
    _packages = [
        ("tomllib", _tomli_parse_value),
        ("tomli", _tomli_parse_value),
        ("toml", _toml_parse_value),
    ]

    def __init__(self):
        loader = None
        decoder = None
        for package, package_decoder in self._packages:
            try:
                loader = importlib.import_module(package)
            except ImportError:
                continue
            else:
                decoder = package_decoder
                break

        if loader is None:
            raise ImportError(
                "No toml parser available. One is included in python 3.11's stdlib default, or "
                "alternatively install `configly[tomli]` or configly[toml]`."
            )

        self.loader = loader
        self.decoder = decoder

    def load(self, value):
        return self.loader.load(value)

    def loads(self, value):
        return self.loader.loads(value)

    def load_value(self, value):
        try:
            return self.decoder(self.loader, value)
        except ValueError:
            return value


Loader = TypeVar("Loader", YamlLoader, JsonLoader, TomlLoader)
