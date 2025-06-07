from core import signalBus
from models.system_thread import SystemThread


class ThreadManager:
    def __init__(self):

        self.__store: dict[str, SystemThread] = {}

        self.connectSignals()

    def prime(self):
        pass

    def launchThread(self, thread: SystemThread):
        if not thread.override() and self.isThreadActive(thread.pid()):
            return  print(f"Thread with id <{thread.pid()}> already running")

        # otherwise override thread
        thread.terminate()
        thread.deleteLater()

        # connect signals
        thread.invoked.connect(self.__handleThreadInvoked)
        thread.completed.connect(self.__handleThreadCompleted)

        # collect the thread
        self.__store[thread.pid()] = thread

        # begin execution
        self.__store[thread.pid()].start()

    def isThreadActive(self, thread_id: str) -> bool:
        thread = self.__store.get(thread_id)
        if thread is None:
            return False
        return thread.isRunning()

    def __handleThreadInvoked(self, threadId: str):
        print("thread started: ", threadId)
        signalBus.ShowProgress.emit(True)


    def __handleThreadCompleted(self, threadId: str):
        print("thread completed: ", threadId)

        if threadId in self.__store.keys():
            thread = self.__store.pop(threadId)

            if thread.failed():
                signalBus.onCreateLog.emit(thread.error())

            # delete it
            thread.deleteLater()

        signalBus.ShowProgress.emit(False)


    def connectSignals(self):
        signalBus.onLaunchThread.connect(self.launchThread)


THREAD_MANAGER = ThreadManager()
