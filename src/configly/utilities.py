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
    """
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        # NOTE:
        #   Single quotes aren't always accepted as valid syntax.
        #   In that case we would rely on the user of this fn to raise a helpful error.
        return value

    return json.dumps(value)
