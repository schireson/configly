import textwrap
from unittest.mock import mock_open, patch

from configly.config import Config
from configly.interpolators.docker_secret import DockerSecretInterpolator
from configly.registry import Registry

registry = Registry()
DockerSecretInterpolator.register(registry)


@patch("os.environ", new={"FOO_FILE": "foo/bar.txt"})
def test_secret_value_opens_file():
    with patch("builtins.open", new=mock_open(read_data=b"meow")) as m:
        config = Config.from_yaml(
            content=textwrap.dedent(
                """
                foo:
                    bar: <% DOCKER_SECRET[foo, 4] %>
                """
            ),
            registry=registry,
        )
    assert config == Config({"foo": {"bar": "meow"}})
    assert m.mock_calls[0].args[0] == "foo/bar.txt"


def test_defaults_value():
    config = Config.from_yaml(
        content=textwrap.dedent(
            """
            foo:
                bar: <% DOCKER_SECRET[foo, 4] %>
            """
        ),
        registry=registry,
    )
    assert config == Config({"foo": {"bar": 4}})
