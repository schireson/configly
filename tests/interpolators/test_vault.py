import json
import textwrap
from unittest.mock import mock_open, patch

import pytest
import responses

from configly.config import Config, post_process
from configly.interpolators.vault import VaultInterpolator
from configly.loaders import YamlLoader

yaml = YamlLoader()


def mock_key_value(key, value=None, status=200):
    if value is None:
        status = 404

    def update(new_value):
        nonlocal value
        value = new_value

    def request_callback(_):
        return (status, {"X-Vault-Index": ""}, json.dumps({"data": json.loads(json.dumps(value))}))

    responses.add_callback(
        responses.GET, f"http://localhost:8200/v1/secret/{key}", callback=request_callback
    )
    return update


@patch.dict("sys.modules", {"hvac": None})
def test_yaml_unavailable():
    with pytest.raises(ImportError) as e:
        VaultInterpolator()
    assert "configly" in str(e.value)


@patch(
    "builtins.open",
    new=mock_open(
        read_data=textwrap.dedent(
            """
            foo:
                bar: <% VAULT[bar, 4] %>
                baz: <% VAULT[baz] %>
            """
        )
    ),
)
@responses.activate
def test_nested_refresh():
    m1 = mock_key_value("bar", 4)
    m2 = mock_key_value("baz", "foo")

    config = Config.from_yaml("foo.yml")
    assert config == Config({"foo": {"bar": 4, "baz": "foo"}})

    m1(13)
    m2("wat")

    config.foo.refresh()
    assert config == Config({"foo": {"bar": 13, "baz": "wat"}})


@responses.activate
def test_missing_key():
    mock_key_value("bar", status=404)

    input = {"bar": "<% VAULT[bar] %>"}
    with pytest.raises(ValueError):
        Config(post_process(yaml, input))


@responses.activate
def test_missing_key_default():
    mock_key_value("bar", status=404)

    input = {"bar": "<% VAULT[bar, 5] %>"}
    config = Config(post_process(yaml, input))
    assert config.bar == 5
