
import logging
from typing import Dict
from typing_extensions import override
from id_listener import IdListener

logging.basicConfig(level=logging.INFO)

class LoggingIdListener(IdListener):
    """implementation of an IdListener that just writes all events to log
    """

    def notify_id_presented(self, id: str, deviceMarker: str) -> None:
        logging.info(f"id: {id} : from {deviceMarker}")
        return super().notify_id_presented(id, deviceMarker)


    def notify_id_removed(self, deviceMarker: str) -> None:
        logging.info(f"cleared device {deviceMarker}")
        return super().notify_id_removed(deviceMarker)
    
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