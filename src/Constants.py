from typing import Mapping
import yaml
from pathlib import Path


with open('config-default.yml', encoding='UTF-8') as f:
    _CONFIG_YAML = yaml.safe_load(f)


def _recursive_update(original, new):
    '''
    Helper method which implements a recursive `dict.update`
    method, used for updating the original configuration with
    configuration specified by the user.
    '''

    for key, value in original.items():
        if key not in new:
            continue

        if isinstance(value, Mapping):
            if not any(isinstance(subvalue, Mapping) for subvalue in value.values()):
                original[key].update(new[key])
            _recursive_update(original[key], new[key])
        else:
            original[key] = new[key]

if Path("config.yml").exists():
    print("Found `config.yml` file, loading constants from it.")
    with open("config.yml", encoding="UTF-8") as f:
        user_config = yaml.safe_load(f)
    _recursive_update(_CONFIG_YAML, user_config)



class YAMLGetter(type):
    subsection = None

    def __getattr__(cls, name):
        name = name.lower()

        try:
            if cls.subsection is not None:
                return _CONFIG_YAML[cls.section][cls.subsection][name]
            return _CONFIG_YAML[cls.section][name]
        except KeyError as e:
            raise AttributeError(f"Configuration value `{name}` not found.") from e
        
    def __setattr__(cls, name, value):
        name = name.lower()

        try:
            if cls.subsection is not None:
                _CONFIG_YAML[cls.section][cls.subsection][name] = value
            else:
                _CONFIG_YAML[cls.section][name] = value
        except KeyError as e:
            raise AttributeError(f"Configuration value `{name}` not found.") from e
    
    def __getitem__(cls, name):
        return cls.__getattr__(name)

    def __iter__(cls):
        '''Return generator of key: value pairs'''
        for name in cls.__annotations__:
            yield name, getattr(cls, name)