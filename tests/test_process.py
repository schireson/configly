import textwrap
from unittest.mock import mock_open, patch

import pytest

from configly.config import Config, post_process
from configly.loaders import YamlLoader

yaml = YamlLoader()


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
