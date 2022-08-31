from simple_id_notifier import SimpleIdNotifier


class CliIdNotifier(SimpleIdNotifier):
    """Simple mock of a card reader that reads ids from CLI
    
    call run to start read loop
    TODO: move loop to thread
    """

    DEVICE_MARKER_TEMPLATE: str = "Cli id notifier:%s"

    def __init__(self):
        self.keep_running = True
        self.deviceMarker = CliIdNotifier.DEVICE_MARKER_TEMPLATE % id(self)

        super().__init__()

    def run(self) -> None:
        while(self.keep_running):
            id_read = input()
            id_read = id_read.strip()
            if(len(id_read) != 0):
                self.notify_id_presented(id_read, self.deviceMarker)
            else:
                self.notify_id_removed(self.deviceMarker)
            




