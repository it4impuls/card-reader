
#reads from 
from id_listener import IdListener
from id_notifier import IdNotifier

from cli_id_notifier import CliIdNotifier
from cog_dbus_ctl_listener import CogDBusCtlListener
from logging_id_listener import LoggingIdListener


import configparser

class ConfigProvider:

    def read(self, filename: str) -> None:
        pass
        
    
    def getNotifiers(self) -> list[IdNotifier]:
        pass

    def getListeners(self) -> list[IdListener]:
        pass



class ConfigProviderIni(ConfigProvider):
    """Default config Provider, using a ini file"""
    DEFAULT_NOTIFIERS = ['CliIdNotifier']
    DEFAULT_LISTENERS = ['LoggingIdListener']

    # @override
    def read(self, filename: str) -> None:
        if filename is None:
            raise ValueError
        config = configparser.ConfigParser()
        config.optionxform = str #config parser usualy normalizes all configs to lowercase, this prevents this behaviour
        # https://stackoverflow.com/a/19359720
        files_read = config.read(filename)
        if len(files_read) < 1:
            raise FileNotFoundError
        notifiersAsStrings = config['notifiers']
        for notifier in notifiersAsStrings:
            print(notifier)
        listenersAsStrings = config['listeners']

        
    def getNotifiers(self) -> list[IdNotifier]:
        return self._toObjects(ConfigProviderIni.DEFAULT_NOTIFIERS, dict())
    
    def getListeners(self) -> list[IdListener]:
        return self._toObjects(ConfigProviderIni.DEFAULT_LISTENERS, dict())
    
    def _toObjects(self, classNames : list[str], config :dict[str,dict[str,str]]) -> list[any]:
        resultObjects = list()
        for className in classNames:
            resultObject = globals()[className]()
            resultObjects.append(resultObject)
        return resultObjects