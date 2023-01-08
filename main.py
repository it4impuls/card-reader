



import logging
import time
from cli_id_notifier import CliIdNotifier
from logging_id_listener import LoggingIdListener
from rdm6300_id_notifier import Rdm3600IdNotifier
from savapage_id_listener import SavapageIdListener
from cog_dbus_ctl_listener import CogDBusCtlListener


def main():
    
    listener1 = LoggingIdListener()
    # listener2 = SavapageIdListener()
    listener3 = CogDBusCtlListener()
    notifier1 = CliIdNotifier()
#     notifier2 = Rdm3600IdNotifier()
    notifier1.add_listener(listener1)
    # notifier1.add_listener(listener2)
    notifier1.add_listener(listener3)
#     notifier2.add_listener(listener1)
#     notifier2.add_listener(listener3)

    # listener2.run()
#     notifier2.run()

#     try:
#         notifier2.join()
#     except KeyboardInterrupt:
#         logging.info("shutting down")
#         notifier2.stop()
#         notifier2.join()
#         logging.info("shutdown complete")







if __name__ == "__main__":
    main()


# if __name__ == "__main__":
#     path_current_directory = os.path.dirname(__file__)
#     path_to_config = os.path.join(path_current_directory,"terminal.ini")
#     config = configparser.ConfigParser()
#     config.read(path_to_config)

#     baseURL = config.get("configs","baseURL")
#     port = config.get("configs","port")
#     heartbeat_interval = float(config.get("configs","heartbeat_interval"))

#     r = TN_Reader(port=port, baseURL=baseURL, heartbeat_interval=heartbeat_interval)
#     r.start()
