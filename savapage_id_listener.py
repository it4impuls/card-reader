import logging
from webbrowser import get
from id_listener import IdListener
import threading
import socket
from xmlrpc.client import ServerProxy

class SavapageIdListener(IdListener):
    """ forwards the Ids to a Savapage instance
    """

    API_ID = "savapage-nfc-reader"
    API_KEY ="302c021447ca02bbfe3234e7d993920c8b2741609b6550be0214116c5704efe9ed019a1ac6374c0a074cae6965c2"

    def __init__(self) -> None:
        self.server_thread = threading.Thread(target=self._server_thread_func, args=(1,))
        self.dont_stop = True
        self._s = None
        super().__init__()

    def run(self):
        """
        starts the communication with a Savapage server
        """
        self.server_thread.start()

    def stop(self):
        """
        stops the communication with a Savapage server
        """
        self.dont_stop = False
        self._s.close()
        self.server_thread.join()
        
    def _server_thread_func(self, name):
        logging.info("server_thread is running")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self._s = s
            s.bind((self._server_host(), self._server_port()))
            s.listen()
            try:
                conn, addr = s.accept()
                with conn:
                    logging.info(f"Request from {addr[0]} port  {addr[0]}")
                    conn.sendall(SavapageIdListener.API_ID.encode('ascii'))

                    

            except (NameError, OSError):
                logging.info("Socket closed")
        
        logging.info("server_thread is stopped")


    def _server_host(self) -> str:
        return "0.0.0.0"
    def _server_port(self) -> int:
        return 8080

    def notify_id_presented(self, id: str, deviceMarker: str) -> None:
        if not isinstance(id, str):
            raise Exception()
        if len(id) <=0:
            raise Exception()
        self._notify_savapage_server(id)
        return super().notify_id_presented(id, deviceMarker)

    def _notify_savapage_server(self, id: str) -> None:
        logging.debug(f"notifying server on id {id}")
        server = "192.168.100.105"
        port = 8631
        uri = f"http://{server}:{port}/xmlrpc"
        with ServerProxy(uri) as server_proxy:
            methodNameWrapper = getattr(server_proxy, "rfid-event") #python can't deal with the '-' in a method name
            result = methodNameWrapper.cardSwipe(SavapageIdListener.API_ID, SavapageIdListener.API_KEY, id)
            logging.info(result)

