from unittest.mock import patch

import pytest

from configly.loaders import JsonLoader, TomlLoader, YamlLoader


@patch.dict("sys.modules", {"toml": None})
def test_toml_unavailable():
    with pytest.raises(ImportError) as e:
        TomlLoader()
    assert "configly" in str(e.value)


def test_toml_loads():
    loader = TomlLoader()
    result = loader.loads("meow = 4")
    assert result == {"meow": 4}


@patch.dict("sys.modules", {"ruamel.yaml": None})
def test_yaml_unavailable():
    with pytest.raises(ImportError) as e:
        YamlLoader()
    assert "configly" in str(e.value)


def test_json_loads():
    loader = JsonLoader()
    result = loader.loads('{"meow": 4}')
    assert result == {"meow": 4}
