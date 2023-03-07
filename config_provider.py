
#reads from 
from id_listener import IdListener
from id_notifier import IdNotifier

from cli_id_notifier import CliIdNotifier
from cog_dbus_ctl_listener import CogDBusCtlListener
from logging_id_listener import LoggingIdListener
from savapage_id_listener import SavapageIdListener
from rdm6300_id_notifier import Rdm3600IdNotifier


import configparser
import json

class ConfigProvider:

    def read(self, filename: str) -> None:
        pass
        
    
    def getNotifiers(self) -> list[IdNotifier]:
        pass

    def getListeners(self) -> list[IdListener]:
        pass


class ConfigProviderJson(ConfigProvider):
    """Default config Provider, using a json file"""
    DEFAULT_NOTIFIERS = ['Rdm3600IdNotifier']
    DEFAULT_LISTENERS = ['CogDBusCtlListener']
    
    def __init__(self):
        self.notifiers = self._toObjects(ConfigProviderJson.DEFAULT_NOTIFIERS, dict())
        self.listeners = self._toObjects(ConfigProviderJson.DEFAULT_LISTENERS, dict())


    # @override
    def read(self, filename: str) -> None:
        if filename is None:
            raise ValueError
        with open(filename) as config_file:
            config = json.load(config_file)

            notifiersAsList = config['notifiers']
            listenersAsList = config['listeners']
            newNotifiers = []
            newListeners = []
            for notifier in notifiersAsList:            
                newNotifiers.append(self._toObject(notifier["type"],notifier["options"] ))
            self.notifiers = newNotifiers
            for listener in listenersAsList:            
                newListeners.append(self._toObject(listener["type"], listener["options"] if  'options' in listener else None))
            self.listeners = newListeners

        
    def getNotifiers(self) -> list[IdNotifier]:
        return self.notifiers
    
    def getListeners(self) -> list[IdListener]:
        return self.listeners
    
    def _toObject(self, className : str, config :dict[str,dict[str,str]] = None) -> list[any]:
        resultObject = globals()[className]()
        if config is not None:
            resultObject.configure(config)
        return resultObject

    def _toObjects(self, classNames : list[str], config :dict[str,dict[str,str]] ) -> list[any]:
        resultObjects = list()
        for className in classNames:
            resultObject = self._toObject(className)
            resultObjects.append(resultObject)
        return resultObjects

class ConfigProviderIni(ConfigProvider):
    """INCOMPLETE config Provider, using a ini file"""
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