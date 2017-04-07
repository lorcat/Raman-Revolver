from PyQt4 import QtCore, QtGui

from Revolver.common import Tester
from Revolver.classes import devices
from Revolver.runnables import getPool, DoorRunner
from Revolver.pytango import getMotorPosition

from Revolver.UI.layout_dialog_calibration import Ui_Dialog



class CalibrationDialog(QtGui.QDialog, Tester, Ui_Dialog):
    # key for motors
    MOTORX = "RAMANX"
    MOTORY = "RAMANY"
    MOTORZ = "RAMANZ"

    # door
    DOOR = "haspllabcl1.desy.de:10000/llab/door/haspllabcl1.01"

    def __init__(self, parent=None):
        Tester.__init__(self)
        super(CalibrationDialog, self).__init__(parent=parent)

        self.setupUi(self)

        self.debug("Initialization of the calibration dialog")

        self._thread_pool = getPool(parent=self)

        # get motor positions and set the corresponding spin boxes
        key = self.MOTORX
        spinbox = self.dsb_rbx
        value = getMotorPosition(devices.DEVICE_PATHS[key])
        if self.testFloat(value):
            spinbox.setValue(value)

        key = self.MOTORY
        spinbox = self.dsb_rby
        value = getMotorPosition(devices.DEVICE_PATHS[key])
        if self.testFloat(value):
            spinbox.setValue(value)

        key = self.MOTORZ
        spinbox = self.dsb_rbz
        value = getMotorPosition(devices.DEVICE_PATHS[key])
        if self.testFloat(value):
            spinbox.setValue(value)

    def calibrate(self, motor, value):
        """
        Calibrates a motor via Sardana
        @return:
        """
        self.debug("Calibrating a motor ({}) to the value ({})".format(motor, value))
        cmdline = "{} calibrate {} {}".format(self.DOOR, motor, value)
        self.parent().jsRunMacro(cmdline)

    def actionSetMotorX(self):
        """
        Calibrates rbx motor
        @return:
        """
        motor = self.MOTORX.lower()
        value = self.dsb_rbx.value()
        self.calibrate(motor, value)

    def actionSetMotorY(self):
        """
        Calibrates rby motor
        @return:
        """
        motor = self.MOTORY.lower()
        value = self.dsb_rby.value()
        self.calibrate(motor, value)

    def actionSetMotorZ(self):
        """
        Calibrates rbz motor
        @return:
        """
        motor = self.MOTORZ.lower()
        value = self.dsb_rbz.value()
        self.calibrate(motor, value)
        
    def actionMotorXzero(self):
        """
        Calibrates rbx motor to zero
        @return:
        """
        motor = self.MOTORX.lower()
        self.calibrate(motor, 0.)

    def actionMotorYzero(self):
        """
        Calibrates rby motor to zero
        @return:
        """
        motor = self.MOTORY.lower()
        self.calibrate(motor, 0.)

    def actionMotorZzero(self):
        """
        Calibrates rbz motor to zero
        @return:
        """
        motor = self.MOTORZ.lower()
        self.calibrate(motor, 0.)