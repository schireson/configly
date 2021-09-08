import json


def quote_string(value: str):
    r"""Add syntactically-correct quotation characters to a string value.

    >>> quote_string("foo")
    '"foo"'

    >>> quote_string("'bar'")
    "'bar'"

    >>> quote_string("ba'z")
    '"ba\'z"'

    >>> quote_string('''q"u'x''')
    '"q\\"u\'x"'

    >>> quote_string('{"log_level": "INFO"}')
    '{"log_level": "INFO"}'
    """
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        # NOTE:
        #   Single quotes aren't always accepted as valid syntax.
        #   And just because a value is surrounded by quotes, does not mean it is correctly quoted.
        #   In that case we would rely on the user of this fn to raise a helpful error.
        return value

    try:
        json.loads(value)
    except json.decoder.JSONDecodeError:
        # If the value is unable to load via json.loads, this means we have to quote it
        # and perform any necessary escaping.
        return json.dumps(value)

    return value
