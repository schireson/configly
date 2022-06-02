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


class TomlLoader:
    def __init__(self):
        try:
            import toml
        except ImportError:
            raise ImportError("Install `configly[toml]` to use the yaml loader.")

        self.loader = toml
        self.decoder = toml.TomlDecoder()

    def load(self, value):
        return self.loader.load(value)

    def loads(self, value):
        return self.loader.loads(value)

    def load_value(self, value):
        try:
            return self.decoder.load_value(value)[0]
        except ValueError:
            return value


Loader = TypeVar("Loader", YamlLoader, JsonLoader, TomlLoader)
