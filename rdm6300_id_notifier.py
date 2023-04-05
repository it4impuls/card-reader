import logging
import threading
from simple_id_notifier import SimpleIdNotifier
import rdm6300


class Rdm3600IdNotifier(SimpleIdNotifier):
    """Reads the Id from a rdm3600 module connected over uart
    
    call run to start read loop
    TODO: move loop to thread
    """

    DEVICE_MARKER_TEMPLATE: str = "Rdm3600 id notifier at %s:%s"

    def __init__(self):
        self.keep_running = True
        self.UartDeviceFile = "/dev/ttyUSB0" #TODO: move to config
        self.deviceMarker = Rdm3600IdNotifier.DEVICE_MARKER_TEMPLATE % (self.UartDeviceFile,id(self))
        self.UartReader = TN_Reader(self, self.UartDeviceFile)
        super().__init__()

    def set_uartdevicefile(self, path_string: str) -> None:
        self.UartDeviceFile = path_string

    def notify_id_presented(self, Id: str) -> None:
        super().notify_id_presented(Id, self.deviceMarker)
    
    def notify_id_removed(self) -> None:
        super().notify_id_removed(self._deviceMarker())

    def _deviceMarker(self) -> str:
        return self.deviceMarker

    def run(self) -> None:
        self._deviceThread = threading.Thread(target=self.UartReader.start)
        self._deviceThread.start()


    def stop(self):
        self.UartReader.stop()



    def join(self) -> None:
        self._deviceThread.join()
            




class TN_Reader(rdm6300.BaseReader):

    def __init__(self, notifierObject: Rdm3600IdNotifier, port: str, heartbeat_interval:float=0.5):
        self._notifierObject = notifierObject
        self.current_id = None

        super().__init__(port, heartbeat_interval=heartbeat_interval)
        
    def card_inserted(self, card) -> None:
        if card.is_valid and self.current_id != card.value:
            self._notifierObject.notify_id_presented(card.value)
            
    

    def card_removed(self, card):
        self._notifierObject.notify_id_removed()

    def invalid_card(self, card):
        logging.error(f"invalid card {card}")




