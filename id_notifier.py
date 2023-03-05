from abc import abstractmethod
from id_listener import IdListener


class IdNotifier:
    """Baseclass for everything that provides ids
    e.g. NFC-Token readers, barcode readers, number pads
    """

    @abstractmethod
    def add_listener(self, listener : IdListener) -> None:
        """ registers a listener to be notified on Id events

        :param listener: the object of a listener
        """

    @abstractmethod
    def remove_listener(self, listener : IdListener) -> None:
        """ removes a registered listener

        :param listener: the object of a listener
        """

    @abstractmethod
    def configure(self, config: dict[str, str]) -> None:
        """
        set the configuration for this notifier

        :param config: configuration values as a dictionary
        """