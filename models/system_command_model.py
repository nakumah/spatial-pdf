from typing import Any

class SystemCommandModel:
    def __init__(self, **kwargs):

        self.__opts: dict[str, Any] = {
            "code": None,
            "params": None,
        }

        self.setOpts(**kwargs)

    def setOpts(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.__opts:
                raise KeyError(f'"{key}" is not a valid option, expected <{self.__opts.keys()}>')
            self.__opts[key] = value

    def opts(self, key: str = None):
        if key is None:
            return self.__opts
        else:
            if key not in self.__opts:
                raise KeyError(f'"{key}" is not a valid option, expected <{self.__opts.keys()}>')
            return self.__opts[key]