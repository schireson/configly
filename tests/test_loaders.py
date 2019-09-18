from unittest.mock import patch

import pytest

from configly.loaders import get_package_name, TomlLoader, YamlLoader


@patch.dict("sys.modules", {"toml": None})
def test_toml_unavailable():
    with pytest.raises(ImportError) as e:
        TomlLoader()
    assert get_package_name() in str(e.value)


@patch.dict("sys.modules", {"ruamel.yaml": None})
def test_yaml_unavailable():
    with pytest.raises(ImportError) as e:
        YamlLoader()
    assert get_package_name() in str(e.value)
