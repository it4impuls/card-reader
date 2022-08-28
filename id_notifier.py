from abc import abstractmethod
from id_listener import IdListener


class IdNotifier:
    """Baseclass for everything that provides ids
    e.g. NFC-Token readers, barcode readers, number pads
    """

    @abstractmethod
    def add_listener(listener : IdListener) -> None:
        """ registers a listener to be notified on Id events

        :param listener: the object of a listener
        """

    @abstractmethod
    def remove_listener(listener : IdListener) -> None:
        """ removes a registered listener

        :param listener: the object of a listener
        """