import logging
import threading
from typing import Dict
from typing_extensions import override
from simple_id_notifier import SimpleIdNotifier
import rdm6300
import pyudev

class Rdm3600IdNotifier(SimpleIdNotifier):
    """Reads the Id from a rdm3600 module connected over uart
    
    call run to start read loop
    TODO: move loop to thread
    """



    DEFAULT_UART_DEVICE = "/dev/ttyUSB0"
    DEVICE_MARKER_TEMPLATE: str = "Rdm3600 id notifier at %s:%s"

    def __init__(self):
        self.keep_running = True
        self.UartDeviceFile = Rdm3600IdNotifier.DEFAULT_UART_DEVICE
        self.preset_usb_device()
        self.UartReader = None
        self.deviceMarker = 'unspecified'
        super().__init__()
    
    def preset_usb_device(self):
        context = pyudev.Context()
        for device in context.list_devices(subsystem='tty'):
            if device.get('ID_VENDOR_ID') == '1a86' and device.get('ID_MODEL_ID') == '7523':
                self.UartDeviceFile = device.get('DEVNAME')
            else:
                pass



    def notify_id_presented(self, Id: str) -> None:
        super().notify_id_presented(Id, self.deviceMarker)
    
    def notify_id_removed(self) -> None:
        super().notify_id_removed(self._deviceMarker())

    def _deviceMarker(self) -> str:
        return self.deviceMarker

    def run(self) -> None:
        self.UartReader = TN_Reader(self, self.UartDeviceFile)
        self._deviceThread = threading.Thread(target=self.UartReader.start)
        self._deviceThread.start()


    def stop(self):
        if self.UartReader is not None:
            self.UartReader.stop()
        else:
            logging.error(f"stopping non existing UartReader")




    def join(self) -> None:
        self._deviceThread.join()
            


    @override
    def configure(self, config: Dict[str, str]) -> None:
        """
        set the configuration for this listener

        :param config: configuration values as a dictionary
        """
        # TODO: hier die urls setzen
        if config is not None:
            for key_pair in config:
                self.__setattr__(key_pair, config[key_pair] )
        self.deviceMarker = Rdm3600IdNotifier.DEVICE_MARKER_TEMPLATE % (self.UartDeviceFile,id(self))




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




