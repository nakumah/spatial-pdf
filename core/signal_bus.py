from PySide6.QtCore import QObject, Signal

class SignalBus(QObject):
    onCreateLog = Signal(object)

signalBus = SignalBus()