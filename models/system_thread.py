import uuid
from typing import Callable, Any

from PySide6 import QtCore
from PySide6.QtCore import Signal


class SystemThread(QtCore.QThread):
    invoked = Signal(str)  # when the process starts
    completed = Signal(str)  # at the end of all processes

    def __init__(self, opts):
        super().__init__()

        # define the runner configurations
        self.__opts: dict[str, Callable[..., Any] | Any] = {
            "on_success": None,
            "on_error": None,
            "on_success_params": None,
            "on_error_params": None,
            "task": None,
            "task_params": None,
            "error": None,
            "has_error": False,
            "id": str(uuid.uuid4()),
            "override": False,
        }
        self.setOpts(**opts)

        # attach the signals
        self.started.connect(lambda x: self.invoked.emit(self.__opts["id"]))
        self.finished.connect(lambda x: self.completed.emit(self.__opts["id"]))

    # re implemented the runner
    def run(self):
        try:
            task = self.__opts["task"]
            if self.__opts["task_params"]:
                res = task(self.__opts["task_params"])
            else:
                res = task()
            self.__handleTaskSuccess(res)
        except Exception as e:
            self.__handleTaskFailed(e)

    # collect the configuration options
    def setOpts(self, **opts):
        for k, v in opts.items():
            if k not in self.__opts:
                raise KeyError(f'"{k}" is not a valid option, Accepted: <{list(self.__opts.keys())}>')
            self.__opts[k] = v

    def __handleTaskSuccess(self, results: Any):

        # if a handler was provided
        if self.__opts["on_success"]:
            successHandler = self.__opts["on_success"]
            if self.__opts["on_success_params"]:
                successHandler(results)
            else:
                successHandler()

        self.__opts["has_error"] = False

    def __handleTaskFailed(self, error: Exception | None):
        # if a handler was provided
        if self.__opts["on_error"]:
            self.__opts["on_error"](error)
            self.__opts["error"] = error
        else:
            self.__opts["error"] = error

        self.__opts["has_error"] = True

    def error(self):
        return self.__opts["error"]

    def pid(self):
        return self.__opts["id"]

    def override(self):
        return self.__opts["override"]

    def failed(self):
        return self.__opts["has_error"]
