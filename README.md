![CircleCI](https://img.shields.io/circleci/build/gh/schireson/configly/master) [![codecov](https://codecov.io/gh/schireson/configly/branch/master/graph/badge.svg)](https://codecov.io/gh/schireson/configly) [![Documentation Status](https://readthedocs.org/projects/configly/badge/?version=latest)](https://configly.readthedocs.io/en/latest/?badge=latest)

## TL;DR

```yaml
# config.yml
foo:
  bar: <% ENV[REQUIRED] %>
  baz: <% ENV[OPTIONAL, true] %>
list_of_stuff:
  - fun<% ENV[NICE, dament] %>al
  - fun<% ENV[AGH, er] %>al
  - more/<% ENV[THAN, er] %>/one/<% ENV[interpolation, er] %>!
```

```python
# app.py
config = Config.from_yaml('config.yml')

print(config.foo.bar)
print(config.foo['baz'])
for item in config.list_of_stuff:
    print(item)
```

```bash
pip install configly[yaml]
```

## Introduction

Loading configuration is done in every (application) project, and yet it is often
overlooked and condidered too easy or straightforward to bother using a library
to manage doing it.

Therefore, we often see code like this:

```python
# config.py
import os

# Maybe it's following 12factor and loading all the config from the environment.
config = {
    'log_level': os.getenv('LOG_LEVEL'),
    'database': {
        # At least here, I can nest values if I want to organize things.
        'password': os.environ['DATABASE_PASSWORD'],
        'port': int(os.environ['DATABASE_PORT']),
    }
}
```

or this

```python
# config.py
import os

class Config:
    log_level = os.getenv('LOG_LEVEL')

    # Here it's not so easy to namespace
    database_password = os.environ['DATABASE_PASSWORD']
    database_port = int(os.environ['DATABASE_PORT'])


# Oh goodness!
class DevConfig(Config):
    environment = 'dev'
```

or this

```python
import configparser
# ...🤢... Okay I dont even want to get into this one.
```

And this is all assuming that everyone is loading configuration at the outermost entrypoint!
The two worst possible outcomes in configuration are:

- You are loading configuration lazily and/or deeply within your application, such that it
  hits a critical failure after having seemingly successfully started up.
- There is not a singular location at which you can go to see all configuration your app might
  possibly be reading from.

## The pitch

`Configly` asserts configuration should:

- Be centralized
  - One should be able to look at one file to see all (env vars, files, etc) which must exist for the
    application to function.
- Be comprehensive
  - One should not find configuration being loaded secretly elsewhere
- Be declarative/static
  - code-execution (e.g. the class above) in the definition of the config inevitably makes it
    hard to interpret, as the config becomes more complex.
- Be namespacable
  - One should not have to prepend `foo_` namespaces to all `foo` related config names
- Be loaded, once, at app startup
  - (At least the _definition_ of the configuration you're loading)
- (Ideally) have structured output
  - If something is an `int`, ideally it would be read as an int.

To that end, the `configly.Config` class exposes a series of classmethods from which your config
can be loaded. It's largely unimportant what the input format is, but we started with formats
that deserialize into at least `str`, `float`, `int`, `bool` and `None` types.

```python
# Currently supported input formats.
config = Config.from_yaml('config.yml')
config = Config.from_json('config.json')
config = Config.from_toml('config.toml')
```

Given an input `config.yml` file:

```yaml
# config.yml
foo:
  bar: <% ENV[REQUIRED] %>
  baz: <% ENV[OPTIONAL, true] %>
list_of_stuff:
  - fun<% ENV[NICE, dament] %>al
  - fun<% ENV[AGH, er] %>al
  - more/<% ENV[THAN, er] %>/one/<% ENV[interpolation, er] %>!
```

A number of things are exemplified in the example above:

- Each `<% ... %>` section indicates an interpolated value, the interpolation can
  be a fragment of the overall value, and multiple values can be interpolated
  within a single value.

- `ENV` is an "interpolator" which knows how to obtain environment variables

- `[VAR]` Will raise an error if that piece of config is not found, whereas
  `[VAR, true]` will default `VAR` to the value after the comma

- Whatever the final value is, it's interpreted as a literal value in the
  format of the file which loads it. I.E. `true` -> python `True`, `1` ->
  python `1`, and `null` -> python `None`.

Now that you've loaded the above configuration:

```python
# app.py
config = Config.from_yaml('config.yml')

# You can access namespaced config using dot access
print(config.foo.bar)

# You have use index syntax for dynamic, or non-attribute-safe key values.
print(config.foo['baz'])

# You can iterate over lists
for item in config.list_of_stuff:
    print(item)

# You can *generally* treat key-value maps as dicts
for key, value in config.foo.items():
    print(key, value)

# You can *actually* turn key-value maps into dicts
dict(config.foo) == config.foo.to_dict()
```

## Installing

```bash
# Basic installation
pip install configly

# To use the yaml config loader
pip install configly[yaml]

# To use the toml config loader
pip install configly[toml]

# To use the vault config loader
pip install configly[vault]
```
