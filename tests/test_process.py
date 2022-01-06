import textwrap
from unittest.mock import mock_open, patch

import pytest

from configly.config import Config, post_process
from configly.loaders import YamlLoader

yaml = YamlLoader()


class Test_post_process:
    @patch("os.environ", new={"bar": "1"})
    def test_env_var_exists_no_default(self):
        input_ = {"foo": {"bar": "<% ENV[bar] %>"}, "bax": "foo", "baz": 5}
        config = Config(post_process(yaml, input_))
        assert config.foo.bar == 1
        assert config.bax == "foo"
        assert config.baz == 5

    @patch("os.environ", new={})
    def test_env_var_doesnt_exist_no_default(self):
        input_ = {"foo": {"bar": "<% ENV[bar] %>"}}
        with pytest.raises(ValueError):
            post_process(yaml, input_)

    @patch("os.environ", new={})
    def test_env_var_doesnt_exist_with_default(self):
        input_ = {"foo": {"bar": "<% ENV[bar, 1] %>"}}
        config = Config(post_process(yaml, input_))
        assert config.foo.bar == 1

    @patch("os.environ", new={"bar": "3"})
    def test_env_var_exists_with_default(self):
        input_ = {"foo": {"bar": "<% ENV[bar, 1] %>"}}
        config = Config(post_process(yaml, input_))
        assert config.foo.bar == 3

    @patch("os.environ", new={"foo": "2", "bar": "3"})
    def test_list(self):
        input_ = {"foo": ["<% ENV[foo, 1] %>", "<% ENV[bar, 1] %>"]}
        config = Config(post_process(yaml, input_))
        assert config.foo == [2, 3]

    def test_invalid_interpolator(self):
        input_ = "<% FART[foo, 1] %>"
        with pytest.raises(ValueError):
            post_process(yaml, input_)

    @patch("builtins.open", new=mock_open(read_data=textwrap.dedent("woah!").encode("utf-8")))
    @patch("os.path.exists", return_value=True)
    def test_file_loader_file_exists(self, _):
        input_ = {"file": "<% FILE[foo.txt, 1] %>"}
        config = Config(post_process(yaml, input_))
        assert config.file == "woah!"

    def test_file_loader_file_doesnt_exist(self):
        input_ = {"file": "<% FILE[bar.txt, 1] %>"}
        config = Config(post_process(yaml, input_))
        assert config.file == "1"


class Test_post_process_type_interpretation:
    @patch("os.environ", new={"foo": "null"})
    def test_null(self):
        input_ = {"foo": "<% ENV[foo] %>"}
        config = Config(post_process(yaml, input_))
        assert config.foo is None

    @patch("os.environ", new={"foo": "true"})
    def test_boolean(self):
        input_ = {"foo": "<% ENV[foo] %>"}
        config = Config(post_process(yaml, input_))
        assert config.foo is True

    @patch("os.environ", new={"foo": "65"})
    def test_integer(self):
        input_ = {"foo": "<% ENV[foo] %>"}
        config = Config(post_process(yaml, input_))
        assert config.foo == 65

    @patch("os.environ", new={"foo": "65.8"})
    def test_float(self):
        input_ = {"foo": "<% ENV[foo] %>"}
        config = Config(post_process(yaml, input_))
        assert config.foo == 65.8

    @patch("os.environ", new={"foo": "abcdef1234"})
    def test_string(self):
        input_ = {"foo": "<% ENV[foo] %>"}
        config = Config(post_process(yaml, input_))
        assert config.foo == "abcdef1234"

    @patch("os.environ", new={"foo": ">abcdef1234"})
    def test_string_with_special_char_prefix(self):
        input_ = {"foo": "<% ENV[foo] %>"}
        config = Config(post_process(yaml, input_))
        assert config.foo == ">abcdef1234"

    @patch("os.environ", new={"foo": "abcdef1234"})
    def test_pre_string_with_special_char_prefix(self):
        input_ = {"foo": "><% ENV[foo] %>"}
        config = Config(post_process(yaml, input_))
        assert config.foo == ">abcdef1234"

    @patch("os.environ", new={"foo": "5"})
    def test_integer_value_with_pre_or_post(self):
        input_ = {
            "foo": {"bar": "1<% ENV[foo] %>", "baz": "<% ENV[foo] %>2", "qux": "1<% ENV[foo] %>2"}
        }
        config = Config(post_process(yaml, input_))
        assert config.foo.bar == 15
        assert config.foo.baz == 52
        assert config.foo.qux == 152

    @patch("os.environ", new={"foo": ">234!"})
    def test_string_value_with_pre_or_post(self):
        input_ = {"foo": "1<% ENV[foo] %>2"}
        config = Config(post_process(yaml, input_))
        assert config.foo == "1>234!2"

    def test_null_default_value(self):
        input_ = {"foo": "<% ENV[foo, null] %>"}
        config = Config(post_process(yaml, input_))
        assert config.foo is None

    def test_null_default_value_with_pre_and_post(self):
        input_ = {"foo": "1<% ENV[foo, null] %>2"}
        config = Config(post_process(yaml, input_))
        assert config.foo == "1null2"

    @patch("os.environ", new={"foo": '{"hello": "world"}'})
    def test_object_values(self):
        input_ = {"foo": "<% ENV[foo] %>"}
        config = Config(post_process(yaml, input_))
        assert type(config.foo) == Config
        assert config.foo.to_dict() == {"hello": "world"}

    @patch("os.environ", new={"foo": "one", "bar": 'two', 'baz': 'three'})
    def test_multiple_matches(self):
        input_ = {"foo": "<% ENV[foo] %>+<% ENV[bar] %>=<% ENV[baz] %>"}
        config = Config(post_process(yaml, input_))
        assert config.to_dict() == {"foo": "one+two=three"}
