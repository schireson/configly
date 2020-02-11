import json

from configly import get_package_name
from configly.registry import register_interpolator


class VaultInterpolator:
    def __init__(self, **kwargs):
        try:
            import hvac
        except ImportError:
            raise ImportError(
                f"Try installing `{get_package_name()}[vault]` to use the vault interpolator"
            )

        self.client = hvac.Client(**kwargs)

    def __getitem__(self, name):
        import hvac

        try:
            result = self.client.secrets.kv.v1.read_secret(name)
        except hvac.exceptions.InvalidPath:
            raise KeyError(name)
        return json.dumps(result["data"])

    def get(self, name, default=None):
        try:
            return self[name]
        except KeyError:
            return default


register_interpolator("VAULT", VaultInterpolator)
