
import logging
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