import json

from configly import get_package_name


class YamlLoader:
    def __init__(self):
        try:
            from ruamel.yaml import YAML
        except ImportError:
            raise ImportError(
                "Install `{package}[yaml]` to use the yaml loader.".format(
                    package=get_package_name()
                )
            )

        yaml = YAML(typ="safe")

        self.decoder = yaml

    def load(self, value):
        return self.decoder.load(value)

    def load_value(self, value):
        return self.decoder.load(value)


class JsonLoader:
    def __init__(self):
        self.decoder = json.JSONDecoder()

    def load(self, value):
        return json.load(value)

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
            raise ImportError(
                "Install `{package}[toml]` to use the yaml loader.".format(
                    package=get_package_name()
                )
            )

        self.loader = toml.load
        self.decoder = toml.TomlDecoder()

    def load(self, value):
        return self.loader(value)

    def load_value(self, value):
        try:
            return self.decoder.load_value(value)[0]
        except ValueError:
            return value
