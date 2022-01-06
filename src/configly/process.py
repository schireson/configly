import re
from collections.abc import Iterable, Mapping

from configly.registry import registry
from configly.utilities import quote_string

INTERPOLATION_REGEX = re.compile(r"(.*)\<%\s*(\w+)\[([\w.]+)(?:,\s*(.+))?\]\s*%>(.*)")


def post_process(loader, value, registry=registry):
    if isinstance(value, Mapping):
        result = {}
        for key, item in value.items():
            result[key] = post_process(loader, item, registry=registry)
        return result

    elif isinstance(value, Iterable) and not isinstance(value, str):
        result = []
        for item in value:
            result.append(post_process(loader, item, registry=registry))
        return result

    else:
        # Repeatedly evaluate the string until there are no interpolation blocks
        while True:
            # The post-interpolation of previous values might coerce them into
            # concrete values, on which no further processing is necessary.
            if not isinstance(value, str):
                break

            match = re.match(INTERPOLATION_REGEX, value)
            if not match:
                break

            groups = match.groups()
            pre, interpolation_type, var_name, default, post = groups

            if interpolation_type not in registry.interpolators:
                raise ValueError("Unrecognized interpolator type: {}".format(interpolation_type))

            interpolator = registry.interpolators[interpolation_type]
            if default is None:
                try:
                    var_value = interpolator[var_name]
                except KeyError:
                    raise ValueError(
                        "The requested {} value '{}' was not found".format(
                            interpolation_type.lower(), var_name
                        )
                    )
            else:
                var_value = interpolator.get(var_name, default)

            result = pre + var_value + post
            if len(result) and not result[0].isalnum():
                # If the first character of `pre` is not alphanumeric, safely quote the result.
                result = quote_string(result)

            if getattr(interpolator, "yaml_safe", True):
                value = loader.load_value(result)
            else:
                value = result

        return value
