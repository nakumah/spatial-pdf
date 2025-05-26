from PySide6.QtCore import QObject, Signal

class SignalBus(QObject):
    onCreateLog = Signal(object)
    TriggerSystemCommand = Signal(object)
    TriggerAlertBanner = Signal(object)
    OpenFile = Signal()
    RecentChanged = Signal()
    PageClicked = Signal(object)
    PageDoubleClicked = Signal(object)
    TriggerFrameless = Signal()

signalBus = SignalBus()