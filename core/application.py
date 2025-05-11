import traceback
import argparse

from typing import Any

from PySide6.QtWidgets import QApplication

from .command_hub import COMMAND_HUB
from .utils import Logger, DATABASE_MANAGER
from .signal_bus import signalBus

class SingletonApplication(QApplication):

    logger = Logger("application")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__startArgs = {
            "file": None,
            "verbose": False,
        }
        self.setStyle("Fusion")

        self.__processArgs()

        # prepare the database
        DATABASE_MANAGER.prime()
        COMMAND_HUB.prime()

    # region getters

    def startArgs(self):
        return self.__startArgs

    # endregion

    # region workers

    def __processArgs(self):
        parser = argparse.ArgumentParser(description="Arguments for Spatial PDF")

        # Positional optional argument
        parser.add_argument(
            "input_file",
            nargs="?",
            help="Optional input file to process."
        )

        # Optional flag
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Run the application in verbose mode."
        )

        args = parser.parse_args()

        # collect the arguments
        self.__startArgs["file"] = args.input_file
        self.__startArgs["verbose"] = args.verbose

    # endregion

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

