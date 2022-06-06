import pytest

from configly.interpolators.env import EnvVarInterpolator
from configly.registry import Registry


def test_clear_registry():
    registry = Registry()
    registry.register_interpolator("ENV", EnvVarInterpolator)

    assert len(registry.interpolators) == 1

    registry.clear_interpolators()
    assert len(registry.interpolators) == 0


def test_duplicate_registration():
    registry = Registry()
    registry.register_interpolator("ENV", EnvVarInterpolator)

    with pytest.raises(ValueError):
        registry.register_interpolator("ENV", EnvVarInterpolator)


def test_register_instance():
    interpolator = EnvVarInterpolator()
    registry = Registry()
    registry.register_interpolator("ENV", interpolator)

    assert registry.interpolators["ENV"] == interpolator
