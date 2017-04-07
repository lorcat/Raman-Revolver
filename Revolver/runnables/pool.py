__author__ = 'Konstantin Glazyrin'
import time

from PyQt4 import QtCore
from Revolver.common import Tester

from PyTango import DevState, DeviceProxy, DevFailed


class ThreadPool(QtCore.QThreadPool, Tester):
    # maximum number of runners
    MAX_THREADS = 5

    # timeout to wait on the runners in ms
    THREAD_TIMEOUT = 3000

    def __init__(self, parent=None):
        Tester.__init__(self)
        QtCore.QThreadPool.__init__(self, parent)

        self.setMaxThreadCount(self.MAX_THREADS)

    def tryStart(self, *args, **kwargs):
        """
        Starts a runner in a thread
        :param runner:
        :return:
        """
        self.debug("Starting a runner ({})".format(args))
        QtCore.QThreadPool.tryStart(self, *args, **kwargs)

    def cleanup(self):
        """
        Cleaning up the procedures
        :return:
        """
        self.waitForDone(self.THREAD_TIMEOUT)

class ProcessRunner(QtCore.QRunnable, Tester):
    """
    Process starting runnable
    """
    def __init__(self, cmd, *args):
        Tester.__init__(self)
        QtCore.QRunnable.__init__(self)

        # save initialization parameters
        self.cmd = cmd
        self.args = args[0]

        if not isinstance(self.args, list) and not isinstance(self.args,tuple):
            self.error("Configuration error; process arguments must be in a list or tuple ({})".format(self.args))
            self.args = []

        self.setAutoDelete(True)

    def run(self):
        """
        Starts a process
        :return:
        """
        self.debug("Starting a process ({}) with arguments ({})".format(self.cmd, self.args))
        proc = QtCore.QProcess()

        proc.startDetached(self.cmd, self.args)

class LambdaRunner(QtCore.QRunnable, Tester):
    """
    Process starting runnable
    """

    def __init__(self, lfunc, response_func=None):
        Tester.__init__(self)
        QtCore.QRunnable.__init__(self)

        # save initialization parameters
        self.cmd = lfunc

        # notification object
        self.emitter = Emmiter()

        self.setAutoDelete(True)

        # prepare a signal to be fired before the end of the runner - to notify parent application
        self.bresponse = False
        if self.test(response_func):
            self.bresponse = True
            self.emitter.connectSignal(response_func)

    def run(self):
        """
        Starts a process
        :return:
        """
        self.debug("Starting a lambda ({})".format(self.cmd))
        self.cmd()

        if self.bresponse:
            self.emitter.emitSignal()


class PytangoRunner(QtCore.QRunnable, Tester):
    """
    Process starting runnable
    """

    def __init__(self, device, attr, value):
        Tester.__init__(self)
        QtCore.QRunnable.__init__(self)

        # save initialization parameters
        self.device = device
        self.attr = attr
        self.value = value

        # notification object
        self.emitter = Emmiter()

        self.setAutoDelete(True)


    def run(self):
        """
        Starts a process
        :return:
        """
        self.debug("Starting a pytango runner ({}/{}/{})".format(self.device, self.attr, self.value))

        try:
            d = DeviceProxy(self.device)
            d.ping()

            state = d.state()
            if state == DevState.FAULT:
                raise DevFailed

            d.write_attribute(self.attr, self.value)
        except DevFailed:
            self.error("Error with the pytango runner ({}/{}/{})".format(self.device, self.attr, self.value))



class DoorRunner(QtCore.QRunnable, Tester):
    """
    Process starting runnable
    """

    def __init__(self, door, args, response_func=None):
        Tester.__init__(self)
        QtCore.QRunnable.__init__(self)

        # save initialization parameters
        self.door = door
        self.args = args

        # notification object
        self.emitter = DoorEmmiter()

        self.setAutoDelete(True)

        # prepare a signal to be fired before the end of the runner - to notify parent application
        self.bresponse = False
        if self.test(response_func):
            self.bresponse = True
            self.emitter.connectSignal(response_func)

    def run(self):
        """
        Starts a process
        :return:
        """
        self.debug("Starting a door command ({}, {})".format(self.door, self.args))

        info, error, output = "", "", ""

        try:
            # connect to the door, run macro
            d = DeviceProxy(self.door)
            state = d.state()

            d.RunMacro(self.args)

            state = d.state()
            while(True):
                time.sleep(0.2)
                if state==DevState.ON or state==DevState.ALARM:
                    break
                state = d.state()

            output = d.read_attribute("output").value
            info = d.read_attribute("info").value
            error = d.read_attribute("error").value
        except (DevFailed, AttributeError) as e:
            output = "Door connection error ({})".format(self.door)
            self.error(output)

        self.debug("Received information from the door \nOutput: {}\nInfo: {}\nError: {}".format(output, info, error))


        if output is None:
            output = []
        if info is None:
            info = []
        if error is None:
            error = []

        if self.bresponse:
            self.emitter.emitSignal(output, info, error)

class Emmiter(QtCore.QObject):
    """
    Class used to hold and emit signals
    """
    sign_finished = QtCore.pyqtSignal()

    def emitSignal(self):
        """
        Emits a signal notifying all connected functions
        @return:
        """
        self.sign_finished.emit()

    def connectSignal(self, func):
        """
        Connects a function to be notified on the signal event
        @param finc:
        @return:
        """
        self.sign_finished.connect(func)

class ValueEmmiter(QtCore.QObject):
    """
    Class used to hold and emit signals
    """
    sign_finished = QtCore.pyqtSignal(object)

    def emitSignal(self, value):
        """
        Emits a signal notifying all connected functions
        @return:
        """
        self.sign_finished.emit(value)

    def connectSignal(self, func):
        """
        Connects a function to be notified on the signal event
        @param finc:
        @return:
        """
        self.sign_finished.connect(func)

class DoorEmmiter(QtCore.QObject):
    """
    Class used to hold and emit signals
    """
    sign_finished = QtCore.pyqtSignal(object, object, object)

    def emitSignal(self, output, info, error):
        """
        Emits a signal notifying all connected functions
        @return:
        """
        self.sign_finished.emit(output, info, error)

    def connectSignal(self, func):
        """
        Connects a function to be notified on the signal event
        @param finc:
        @return:
        """
        self.sign_finished.connect(func)



THREAD_POOL = None

def getPool(parent=None):
    global THREAD_POOL
    if THREAD_POOL is None:
        THREAD_POOL = ThreadPool(parent=parent)
    return THREAD_POOL