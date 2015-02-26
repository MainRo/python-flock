from unittest import TestCase
from mock import patch

from flock.controller_factory import ControllerFactory
from flock.controller.rfxcom.transport import RfxcomTransport

from twisted.internet import reactor

class ControllerFactoryTestCase(TestCase):

    @patch('os.path.exists', return_value=False)
    def test_init(self, mock_path_exists):
        factory = ControllerFactory(reactor)

    @patch('flock.controller_factory.RfxcomTransport')
    @patch('os.path.exists', return_value=True)
    @patch('os.listdir',
            return_value=['usb-RFXCOM_RFXtrx433_XXXR4242-if00-port0'])
    @patch('flock.controller_factory.Router')
    def test_coldplug_rfxcom(self, mock_router, mock_listdir, mock_path_exists, mock_rfxcom):
        mock_router.instantiate.return_value = mock_router
        factory = ControllerFactory(reactor)
        self.assertEqual(1, mock_router.attach_controller.call_count)

    @patch('os.path.exists', return_value=True)
    @patch('os.listdir',
            return_value=['usb-UNKNOWN-if00-port0'])
    @patch('flock.controller_factory.Router')
    def test_coldplug_unknown_controller(self, mock_router, mock_listdir, mock_path_exists):
        mock_router.instantiate.return_value = mock_router
        factory = ControllerFactory(reactor)
        self.assertEqual(0, mock_router.attach_controller.call_count)

    @patch('flock.controller_factory.EnoceanTransport')
    @patch('flock.controller_factory.RfxcomTransport')
    @patch('os.path.exists', return_value=True)
    @patch('os.listdir',
            return_value=['usb-RFXCOM_RFXtrx433_XXXR4242-if00-port0',
                          'usb-EnOcean_GmbH_EnOcean_USB_300_DA_XXXX4242-if00-port0'])
    @patch('flock.controller_factory.Router')
    def test_coldplug_rfxcom_enocean(self, mock_router, mock_listdir,
            mock_path_exists, mock_rfxcom, mock_enocean):
        mock_router.instantiate.return_value = mock_router
        factory = ControllerFactory(reactor)
        self.assertEqual(2, mock_router.attach_controller.call_count)

