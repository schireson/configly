import textwrap
from unittest.mock import mock_open, patch

import pytest

from configly.config import Config


def test_empty_config():
    Config()


@patch(
    "builtins.open",
    new=mock_open(
        read_data=textwrap.dedent(
            """
            foo:
                bar: <% ENV[bar, 4] %>
            """
        )
    ),
)
def test_yaml():
    config = Config.from_yaml("foo.yml")
    assert config.foo.bar == 4


@patch(
    "builtins.open",
    new=mock_open(
        read_data=textwrap.dedent(
            """
            [foo]
            bar = "<% ENV[var, 4] %>"
            baz = "a<% ENV[foo, 4] %>sdf"
            """
        )
    ),
)
def test_toml():
    config = Config.from_toml("foo.toml")
    assert config.foo.bar == 4
    assert config.foo.baz == "a4sdf"


@patch(
    "builtins.open",
    new=mock_open(
        read_data=textwrap.dedent(
            """
            {
                "foo": {
                    "bar": "<% ENV[foo, 4] %>",
                    "baz": "a<% ENV[foo, 4] %>sdf"
                }
            }
            """
        )
    ),
)
def test_json():
    config = Config.from_json("foo.json")
    assert config.foo.bar == 4
    assert config.foo.baz == "a4sdf"


class TestConfig:
    def test_to_dict(self):
        result = Config({"foo": "bar"}).to_dict()
        assert result == {"foo": "bar"}

    def test_iterable(self):
        config = Config({"foo": "bar", "bar": {"nested": 4}})

        items = list(config)
        assert sorted(items) == [("bar", Config({"nested": 4})), ("foo", "bar")]

    def test_static_lookup(self):
        config = Config({"foo": "bar", "bar": {"nested": 4}})
        assert config.bar.nested == 4

    def test_static_lookup_missing(self):
        config = Config({})
        with pytest.raises(AttributeError):
            config.bar

    def test_dyanmic_lookup(self):
        config = Config({"foo": "bar", "bar": {"nested": 4}})
        assert config["bar"]["nested"] == 4

    def test_dynamic_lookup_missing(self):
        config = Config({})
        with pytest.raises(KeyError):
            config["bar"]

    def test_attribute_passthrough(self):
        config = Config({"bar": 4})
        assert list(config.items()) == [("bar", 4)]

    def test_equality(self):
        config = Config({"bar": 4})
        config2 = Config({"bar": 4})
        raw_data = {"bar": 4}

        config3 = Config({"bar": 5})

        assert config == config2
        assert config == raw_data
        assert config != config3

    @patch(
        "builtins.open",
        new=mock_open(
            read_data=textwrap.dedent(
                """
                foo:
                    bar: <% ENV[bar, 4] %>
                """
            )
        ),
    )
    def test_refresh(self):
        config = Config.from_yaml("foo.yml")
        config.refresh()

        assert config == Config({"foo": {"bar": 4}})

    @patch(
        "builtins.open",
        new=mock_open(
            read_data=textwrap.dedent(
                """
                foo:
                    bar: <% ENV[bar, 4] %>
                """
            )
        ),
    )
    def test_nested_refresh(self):
        config = Config.from_yaml("foo.yml")
        config.foo.refresh()

        assert config == Config({"foo": {"bar": 4}})
