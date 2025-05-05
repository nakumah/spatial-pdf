import traceback

from typing import Any

from PySide6.QtWidgets import QApplication

from .utils import Logger
from .signal_bus import signalBus

class SingletonApplication(QApplication):

    logger = Logger("application")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setStyle("Fusion")

    # region event handler
    def __handleCreateLogEntry(self, data: Any):
        try:
            if isinstance(data, Exception):
                message = f"{str(data)} \n {''.join(traceback.format_tb(data.__traceback__))}"
                self.logger.error(message, True)

            if isinstance(data, str):
                self.logger.info(data)

            if isinstance(data, dict):
                mode = data.get("mode")
                if mode is None:
                    mode = data.get("type")

                text = data.get("text")
                if text is None:
                    msg = (
                        "Poorly formatted parameter. dict must contain keys - text: str, type: 'error' | 'event' | "
                        "'warning' | None")
                    raise Exception(msg)
                if mode is None:
                    self.logger.info(text)
                if mode == "error":
                    self.logger.error(text, True)
                if mode == "warning":
                    self.logger.warning(text)
                if mode == "event":
                    self.logger.info(text)
        except Exception as e:
            self.logger.error(e, True)

    # endregion

    # region Signals

    def __connectSignals(self):
        signalBus.onCreateLogEntry.connect(self.__handleCreateLogEntry)
    # endregion


def exception_hook(exception: BaseException, value, tb):
    """ exception callback function """
    SingletonApplication.logger.error("Unhandled exception", (exception, value, tb))
    # message = '{0}: {1}'.format(exception.__name__, value)

