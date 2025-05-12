from typing import Callable, Any

from core import signalBus
from core.structs import SYSTEM_ACTIONS
from core.utils import Logger
from models.system_command_model import SystemCommandModel


class CommandHub:
    """
    Manages all global application functions. Such as menu toggling, and non-main thread heavy tasks
    """
    logger = Logger("command_hub")

    def __init__(self):
        super().__init__()

        self.__fxn: dict[SYSTEM_ACTIONS, Callable[..., Any]] = {}

        self.__connectSignals()

    #region initialize

    def prime(self):
        """
        initialize the command hub
        @return:
        """
        self.__fxn: dict[SYSTEM_ACTIONS, Callable[..., Any]] = {
            SYSTEM_ACTIONS.OPEN: self.__openFile,
            SYSTEM_ACTIONS.USER_SETTINGS: self.__settingsDialog,
        }

    # endregion
    
    # region tasks
    def __openFile(self, _=None):
        signalBus.OpenFile.emit()

    def __settingsDialog(self, _=None):
        signalBus.TriggerAlertBanner.emit("Settings dialog not implemented yet.")
    # endregion

    #region event handler

    def executeCommand(self, model: SystemCommandModel | SYSTEM_ACTIONS):
        if isinstance(model, SYSTEM_ACTIONS):
            task = self.__fxn.get(model)
            if task is None:
                raise KeyError(f"Task not found for command <{model}>. Expected <{self.__fxn.keys()}>")
            task()

        if isinstance(model, SystemCommandModel):
            # for tasks belonging to the command hub
            task = self.__fxn.get(model.opts("code"))
            if task is None:
                raise KeyError(f"Task not found for command <{model}>. Expected <{self.__fxn.keys()}>")
            task(model.opts("params"))

    # endregion

    #region connect signal

    def __connectSignals(self):
        signalBus.TriggerSystemCommand.connect(self.executeCommand)

    # endregion


COMMAND_HUB = CommandHub()