



import logging
import os
from config_provider import ConfigProviderJson

from pathlib import Path

def main():


    config = ConfigProviderJson()
    configDirPath = Path.home()
    try:
        configDirPath = Path(os.getenv('SNAP_COMMON'))
    except:
        configDirPath = Path.cwd()
    expectedConfigPath = configDirPath.joinpath("config.json")
    try:
        config.read(expectedConfigPath)
    except Exception as e:
        logging.error(f"no config file found at {expectedConfigPath}. using defaults.")
        logging.error(e)
    notifiers = config.getNotifiers()
    listeners = config.getListeners()
    for notifier in notifiers:
        for listener in listeners:
            notifier.add_listener(listener)
    
    for notifier in notifiers:
        notifier.run()
    for listener in listeners:
        try:
            listener.run()
        except:
            pass




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



