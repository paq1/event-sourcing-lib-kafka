from threading import Thread

from event_sourcing.app.listeners.commands_listener import CommandsListener


class ThreadListenerCommands(Thread):
    def __init__(self, commands_listener: CommandsListener[str]):
        super().__init__()
        self.commands_listener = commands_listener

    def run(self):
        self.commands_listener.run()

    def stop(self):
        print("[ThreadListenerCommands#stop] Stopping listener...")
        print("[ThreadListenerCommands#stop] listener stopped")
