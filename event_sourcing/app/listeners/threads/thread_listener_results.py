from threading import Thread

from event_sourcing.app.listeners.results_listener import ResultsListener


class ThreadListenerResults(Thread):
    def __init__(self, results_listener: ResultsListener[str]):
        super().__init__()
        self.results_listener = results_listener

    def run(self):
        self.results_listener.run()

    def stop(self):
        print("[ThreadListenerCommands#stop] Stopping listener...")
        print("[ThreadListenerCommands#stop] listener stopped")
