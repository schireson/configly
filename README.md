# Configly
A package to simplify and centralize the loading of configuration, such as
environment variables.


## Installation
```bash
# Basic installation
pip install configly

# To use the yaml config loader
pip install configly[yaml]

# To use the toml config loader
pip install configly[toml]
```


## Usage
There are two built in macros `ENV` and `FILE`. In all cases, the result of the macro will
replace it with the evaluated value at that location in the config.

* `<% ENV[NAME]` will load environment variable `NAME` and loudly fail if not found.
* `<% ENV[NAME, default]` will load an environment variable fall back to `'default'` if not found.
* `<% FILE[foo.txt]` will get the file contents of `foo.txt` and fail loudly if not found.
* `<% FILE[foo.txt, default]` will get the file contents of `foo.txt` fall back to `'default'` if not found.

```yaml
# config.yml
foo:
    bar: <% ENV[REQUIRED] %>
    baz: <% ENV[OPTIONAL, true] %>
list_of_stuff:
    - fun<% ENV[NICE, dament] %>al
    - fun<% ENV[AGH, er] %>al
```

```python
config = Config.from_yaml('config.yml')

# foo.bar is guaranteed to exist with a value, because it had no default
print(config.foo.bar)

# Index lookups work too, this one had a default to `True`
print(config.foo['baz'])

for item in config.list_of_stuff:
    print(item)
# assuming neither env vars were set, prints: fundamental, then funeral
```
