


from abc import abstractmethod


class IdListener:
    """Baseclass for everything that can provide us with an Id 
    e.g. NFC-Token readers, barcode readers, number pads
    """

    @abstractmethod
    def notify_id_presented(id: str, deviceMarker: str):
        """
        notify_id_presented is called a new id becomes known

        :param id: the id presented
        :param deviceMarker: something to identify the origin device in case we are listening to several
        """

    @abstractmethod
    def notify_id_removed(deviceMarker: str):
        """
        notify_id_removed is called when the id readout is cleared
        e.g. because the card was removed

        :param deviceMarker: something to identify the origin device in case we are listening to several
        """