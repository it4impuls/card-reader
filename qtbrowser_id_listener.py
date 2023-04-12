from id_listener import IdListener
from typing_extensions import override
from typing import Dict
import logging
from threading import Thread


from PySide2.QtCore import QUrl, QThread, QRunnable, QThreadPool
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QApplication

import os
import sys

# https://stackoverflow.com/questions/10991991/pyside-easier-way-of-updating-gui-from-another-thread



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):   

        super(MainWindow, self).__init__(parent)
        
        self.webEngineView = QWebEngineView()
        self.setCentralWidget(self.webEngineView)
        initialUrl = "https://www.autodesk.com"

        self.webEngineView.load(QUrl(initialUrl))
        self.thread = URLUpdateThread(self)
        self.thread.view = self

        self._invoker = Invoker(self)
        # self.webEngineView.load(initialUrl)
        # self.thread.setWebEngine(self.webEngineView)
        # self.webEngineView.load(QUrl("http://www.google.de"))


    def closeEvent(self, event):
        """
        TODO: find a moreclean solution
        """
        os._exit(0)

    def keyPressEvent(self, event):
        # Re-direct ESC key to closeEvent
        self.close()
        # if event.key() == Key_Escape:
        #     self.close()
        # elif event.key() == QKeySequence.Copy:
        #     self.actionCopy.trigger()

    def invoke_in_main_thread(self, fn, *args, **kwargs):
        QtCore.QCoreApplication.postEvent(self._invoker,
            InvokeEvent(fn, *args, **kwargs))

    def setUrl(self, url: QUrl):
        self.thread.view = self
        self.thread.url = url 
        #self.thread.start()
        self.invoke_in_main_thread(self.updateUrlForView, url)


    def updateUrlForView(self, url):
        self.webEngineView.load(QUrl(url))


class QtBrowserIdListener(IdListener):
    """opens a window showing a webview and allows to set the url for it,
    based on the id provided.
    """

    ON_KEY_PRESENTED_URL_TEMPLATE = "http://mealplan.impulsreha.local:8000/start/{Id}"
    ON_KEY_REMOVED_URL_TEMPLATE = "http://mealplan.impulsreha.local:8000/"

    def __init__(self):

        self.ON_KEY_PRESENTED_URL_TEMPLATE = QtBrowserIdListener.ON_KEY_PRESENTED_URL_TEMPLATE
        self.ON_KEY_REMOVED_URL_TEMPLATE = QtBrowserIdListener.ON_KEY_REMOVED_URL_TEMPLATE
       
    def _getUrlForId(self, id: str) -> str:
        urlForId = self.ON_KEY_PRESENTED_URL_TEMPLATE.format(Id = id)
        logging.info(f"providing key removed url:{urlForId}")
        return urlForId  

    def _getDefaultUrl(self) -> str:
        logging.info(f"providing key removed url:{self.ON_KEY_REMOVED_URL_TEMPLATE}")
        return self.ON_KEY_REMOVED_URL_TEMPLATE

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

    def notify_id_presented(self, id: str, deviceMarker: str) -> None:
        """
        notify_id_presented is called a new id becomes known

        :param id: the id presented
        :param deviceMarker: something to identify the origin device in case we are listening to several
        """
        url = self._getUrlForId(id)
        logging.debug(f"Id presented, Calling {url}")
        self._setUrl(url)


    def notify_id_removed(self, deviceMarker: str) -> None:
        """
        notify_id_removed is called when the id readout is cleared
        e.g. because the card was removed

        :param deviceMarker: something to identify the origin device in case we are listening to several
        """
        url = self._getDefaultUrl()
        logging.debug(f"Id removed, Calling {url}")
        self._setUrl(url)

    def _setUrl(self, url:str):
        self.view.setUrl(url)


    def _createWebView(self):
        self.app = QApplication()
        self.view = MainWindow()
        self.view.showFullScreen()
        # Thread(target=self.app.exec_).start()
        _invoker = Invoker()
        sys.exit(self.app.exec_())

    def run(self):
        """
        make the webview wisible
        """
        Thread(target=self._createWebView).start()

    def stop(self):
        """
        stops the communication with a Savapage server
        """
        self.app.exit()



class URLUpdateThread(QThread):
    def run(self):
        invoke_in_main_thread(self.view.updateUrlForView, self.url)

class InvokeEvent(QtCore.QEvent):
    EVENT_TYPE = QtCore.QEvent.Type(QtCore.QEvent.registerEventType())

    def __init__(self, fn, *args, **kwargs):
        QtCore.QEvent.__init__(self, InvokeEvent.EVENT_TYPE)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs


class Invoker(QtCore.QObject):
    def event(self, event):
        event.fn(*event.args, **event.kwargs)

        return True




