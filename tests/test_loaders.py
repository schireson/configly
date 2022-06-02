import sys
from unittest.mock import patch

import pytest

from configly.loaders import JsonLoader, TomlLoader, YamlLoader


@patch.dict("sys.modules", {"toml": None, "tomli": None, "tomllib": None})
def test_toml_unavailable():
    with pytest.raises(ImportError) as e:
        TomlLoader()
    assert "configly" in str(e.value)


@pytest.mark.skipif(sys.version_info < (3, 11), reason="requires python3.11 or higher")
@patch.dict("sys.modules", {"toml": None, "tomli": None})
def test_fallback_to_tomllib():
    loader = TomlLoader()
    result = loader.loads("foo = 4")
    assert result == {"foo": 4}


@patch.dict("sys.modules", {"toml": None, "tomllib": None})
def test_fallback_to_tomli():
    loader = TomlLoader()
    result = loader.loads("foo = 4")
    assert result == {"foo": 4}

    result = loader.load_value("4")
    assert result == 4


@patch.dict("sys.modules", {"tomli": None, "tomllib": None})
def test_fallback_to_toml():
    loader = TomlLoader()
    result = loader.loads("foo = 4")
    assert result == {"foo": 4}

    result = loader.load_value("4")
    assert result == 4


def test_toml_loads():
    loader = TomlLoader()
    result = loader.loads("meow = 4")
    assert result == {"meow": 4}

    result = loader.load_value("4")
    assert result == 4


@patch.dict("sys.modules", {"ruamel.yaml": None})
def test_yaml_unavailable():
    with pytest.raises(ImportError) as e:
        YamlLoader()
    assert "configly" in str(e.value)


def test_json_loads():
    loader = JsonLoader()
    result = loader.loads('{"meow": 4}')
    assert result == {"meow": 4}
