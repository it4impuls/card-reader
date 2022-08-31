import logging
import time
import unittest
from unittest.mock import patch

# import context
from savapage_id_listener import SavapageIdListener

class SavapageIdListenerTest(unittest.TestCase):


    
    def test_createListener(self):
        listener = SavapageIdListener()
        listener.run()
        time.sleep(1)
        listener.stop()

    def test_runListenerTwice(self):
        listener = SavapageIdListener()
        listener.run()
        self.assertRaises(Exception, listener.run)

    def test_notifyIdPresentedNone(self):
        listener = SavapageIdListener()
        self.assertRaises(Exception, listener.notify_id_presented, None, None)

    def test_notifyIdPresentedEmpty(self):
        listener = SavapageIdListener()
        self.assertRaises(Exception, listener.notify_id_presented, "", None)

    @patch.object(SavapageIdListener, '_notify_savapage_server')
    def test_notifyIdPresented(self, mock):
        listener = SavapageIdListener()
        id = "123"
        listener.notify_id_presented( id, None)
        self.assertTrue(mock.called)
        mock.assert_called_with(id)


    def test__notify_savapage_server(self):
        listener = SavapageIdListener()
        id = "123456789"
        listener._notify_savapage_server( id)
        # self.assertTrue(mock.called)
        # mock.assert_called_with(id)







if __name__ == '__main__':
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    unittest.main()