



import logging
import time
from cli_id_notifier import CliIdNotifier
from config_provider import ConfigProviderJson
from logging_id_listener import LoggingIdListener
from rdm6300_id_notifier import Rdm3600IdNotifier
from savapage_id_listener import SavapageIdListener
from cog_dbus_ctl_listener import CogDBusCtlListener
from pathlib import Path

def main():


    config = ConfigProviderJson()
    try:
        config.read(Path.home().joinpath("config.json"))
    except:
        logging.info("no config file found. using defaults")
    notifiers = config.getNotifiers()
    listeners = config.getListeners()
    for notifier in notifiers:
        for listener in listeners:
            notifier.add_listener(listener)
    
    for notifier in notifiers:
        notifier.run()




    try:
        for notifier in notifiers:
            notifier.join()

    except KeyboardInterrupt:
        logging.info("shutting down")
        for notifier in notifiers:
            notifier.stop()
        for notifier in notifiers:
            notifier.join()

        logging.info("shutdown complete")







if __name__ == "__main__":
    main()



