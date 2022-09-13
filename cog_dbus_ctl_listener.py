import logging
from id_listener import IdListener
import dbus


class CogDBusCtlListener(IdListener):
    """ uses the id as part of a web url that is then assigned
    to the cog instance over dbus
    """

    ON_KEY_PRESENTED_URL_TEMPLATE = "https://www.google.com/search?q={Id}"
    ON_KEY_REMOVED_URL_TEMPLATE = "https://www.google.com/"
    DBUS_OBJECT_NAME = "/com/igalia/Cog"
    DBUS_ADDRESS = "com.igalia.Cog"

    def __init__(self) -> None:
        logging.info("beginning dbus setup")
        self.system_bus = dbus.SystemBus()
        self.connection = self.system_bus.get_object('com.igalia.Cog', '/com/igalia/Cog')
        self.actions = dbus.Interface(self.connection, dbus_interface='org.gtk.Actions')
        logging.info("dbus setup complete")


    def _getUrlForId(self, id: str) -> str:
        urlForId = CogDBusCtlListener.ON_KEY_PRESENTED_URL_TEMPLATE.format(Id = id) 
        return urlForId  

    def _getDefaultUrl(self) -> str:
        return CogDBusCtlListener.ON_KEY_REMOVED_URL_TEMPLATE


    def notify_id_presented(self, id: str, deviceMarker: str) -> None:
        """
        notify_id_presented is called a new id becomes known

        :param id: the id presented
        :param deviceMarker: something to identify the origin device in case we are listening to several
        """
        url = self._getUrlForId(id)
        logging.debug(f"Id presented, Calling {url}")
        self.actions.Activate("open", [url], [])


    def notify_id_removed(self, deviceMarker: str) -> None:
        """
        notify_id_removed is called when the id readout is cleared
        e.g. because the card was removed

        :param deviceMarker: something to identify the origin device in case we are listening to several
        """
        url = self._getDefaultUrl()
        logging.debug(f"Id removed, Calling {url}")
        self.actions.Activate("open", [url], [])


    # def run(self):
    #     """
    #     starts the communication with a Savapage server
    #     """
    #     self.server_thread.start()

    # def stop(self):
    #     """
    #     stops the communication with a Savapage server
    #     """
    #     self.dont_stop = False
    #     self._s.close()
    #     self.server_thread.join()
   



