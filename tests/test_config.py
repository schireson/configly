import textwrap
from unittest.mock import mock_open, patch

import pytest

from configly.config import Config, post_process
from configly.loaders import YamlLoader

yaml = YamlLoader()


def test_empty_config():
    Config()


class Test_post_process:
    @patch("os.environ", new={"bar": "1"})
    def test_env_var_exists_no_default(self):
        input = {"foo": {"bar": "<% ENV[bar] %>"}, "bax": "foo", "baz": 5}
        config = Config(post_process(yaml, input))
        assert config.foo.bar == 1
        assert config.bax == "foo"
        assert config.baz == 5

    @patch("os.environ", new={})
    def test_env_var_doesnt_exist_no_default(self):
        input = {"foo": {"bar": "<% ENV[bar] %>"}}
        with pytest.raises(ValueError):
            post_process(yaml, input)

    @patch("os.environ", new={})
    def test_env_var_doesnt_exist_with_default(self):
        input = {"foo": {"bar": "<% ENV[bar, 1] %>"}}
        config = Config(post_process(yaml, input))
        assert config.foo.bar == 1

    @patch("os.environ", new={"bar": "3"})
    def test_env_var_exists_with_default(self):
        input = {"foo": {"bar": "<% ENV[bar, 1] %>"}}
        config = Config(post_process(yaml, input))
        assert config.foo.bar == 3

    @patch("os.environ", new={"foo": "2", "bar": "3"})
    def test_list(self):
        input = {"foo": ["<% ENV[foo, 1] %>", "<% ENV[bar, 1] %>"]}
        config = Config(post_process(yaml, input))
        assert config.foo == [2, 3]

    def test_invalid_interpolator(self):
        input = "<% FART[foo, 1] %>"
        with pytest.raises(ValueError):
            post_process(yaml, input)

    @patch("builtins.open", new=mock_open(read_data=textwrap.dedent("woah!").encode("utf-8")))
    @patch("os.path.exists", return_value=True)
    def test_file_loader_file_exists(self, _):
        input = {"file": "<% FILE[foo.txt, 1] %>"}
        config = Config(post_process(yaml, input))
        assert config.file == "woah!"

    def test_file_loader_file_doesnt_exist(self):
        input = {"file": "<% FILE[bar.txt, 1] %>"}
        config = Config(post_process(yaml, input))
        assert config.file == "1"


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
