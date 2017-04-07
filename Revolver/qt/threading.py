__author__ = 'Konstantin Glazyrin'

from PyQt4 import QtCore
from PyTango import DeviceProxy, DevFailed
from Revolver.classes.devices import TangoDevice

MAINTHREADPOOL = None

# simple classes to Threaderize attribute writing

class CustomFastThreadPool(QtCore.QThreadPool):
    MAXTREADCOUNT = 20
    def __init__(self, parent=None):
        QtCore.QThreadPool.__init__(self, parent=parent)

        self.__init_variables()

    def __init_variables(self):
        global  MAINTHREADPOOL

        if MAINTHREADPOOL is None:
            MAINTHREADPOOL = self

        self.setMaxThreadCount(self.MAXTREADCOUNT)

    def getDefaultInstance(self):
        global MAINTHREADPOOL
        return MAINTHREADPOOL

class CustomRunnableAttributeWrite(QtCore.QRunnable):
    def __init__(self, devicePath=None, attr=None, value=None):
        QtCore.QRunnable.__init__(self)

        self.__devicePath = devicePath
        self.__attr = attr
        self.__value = value

        self.__init_variables()

    def __init_variables(self):
        self.device = None
        self.setAutoDelete(True)

    def _check(self, value, type=None):
        res = False
        if type is not None and isinstance(value, type):
            res = True
        elif value is not None:
            res = True
        return res

    def _check_str(self, value):
        res = False
        if self._check(value, str) or self._check(value, unicode):
            res = True
        return res

    def isValidDevice(self):
        res = False
        if self._check(self.device, TangoDevice):
            res = True
        return res

    def run(self):
        if self._check_str(self.__devicePath) and self._check_str(self.__attr) and self._check(self.__value):
            try:
                self.device = TangoDevice(self.__devicePath)
                self.device.state()
            except DevFailed:
                self.device = None

            if self.isValidDevice():
                try:
                    self.device.write_attributes_async([[self.__attr, self.__value]])
                except DevFailed:
                    pass
