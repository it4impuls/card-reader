



import logging
import time
from cli_id_notifier import CliIdNotifier
from config_provider import ConfigProviderIni
from logging_id_listener import LoggingIdListener
from rdm6300_id_notifier import Rdm3600IdNotifier
from savapage_id_listener import SavapageIdListener
from cog_dbus_ctl_listener import CogDBusCtlListener


def main():


    config = ConfigProviderIni()
    notifiers = config.getNotifiers()
    lesteners = config.getListeners()
    for notifier in notifiers:
        for listener in lesteners:
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



