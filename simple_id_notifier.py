

from typing import List
from id_listener import IdListener
from id_notifier import IdNotifier


class SimpleIdNotifier(IdNotifier):
    """Implementation of IdNotifer that manages the listeners with list
    """
    def __init__(self):
        """creates the internal list"""
        self._listener_list: List[IdListener] = []

    def add_listener(self, listener: IdListener) -> None:
        self._listener_list.append(listener)
        return super().add_listener(listener)


    def remove_listener(self, listener: IdListener) -> None:
        self._listener_list.remove(listener)
        return super().remove_listener(listener)


    def notify_id_presented(self, Id: str, deviceMarker: str):
        for listener in self._listener_list:
            listener.notify_id_presented(Id, deviceMarker)

    def notify_id_removed(self, deviceMarker: str) -> None:
        for listener in self._listener_list:
            listener.notify_id_removed(deviceMarker)


