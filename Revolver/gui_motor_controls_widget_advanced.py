"""
Motor widget.
Populate motor position to user, which can be changed.
User can also stop all movements of selected motor.
Motor status is signalized by diode.
"""

# import global classes 
import signal
import sys

from PyQt4 import QtGui, Qt
# Import local classes
from Revolver.UI import layout_motor_widget
import Revolver.gui_default_controls_widget as default_gui
import Revolver.gui_device_status_led_widget as led_widget
from Revolver.classes import devices, signals, dialogs
from Revolver.config import config_global as config

# settings for the motor names
KEYMS_STEPS, KEYMS_NAMES = 'STEPS', 'NAMES'
STEP_SETTINGS = [
    # default
    {KEYMS_NAMES: [],
     KEYMS_STEPS: [0.010, 0.001, 0.002, 0.005, 0.010, 0.015, 0.020, 0.025, 0.050, 0.100, 0.2, 0.25, 0.5, 1, 2, 3, 4, 5, 20, 100, 200]
     },
    # custom
    {KEYMS_NAMES: ['zoom'],
     KEYMS_STEPS: [100]
     }
]


class MotorWidget(layout_motor_widget.Ui_Form, default_gui.DefaultControls):
    """
    Basic control widget for motor device
    """

    def __init__(self, parent=None, devicePath=None, device=None):
        super(MotorWidget, self).__init__()
        default_gui.DefaultControls.__init__(self, parent=parent, devicePath=devicePath)

        if device is not None:
            self.defaultMotorDevice = device
        else:
            if devicePath is not None and (isinstance(devicePath, str) or isinstance(devicePath, unicode)):
                self.defaultMotorDevice = devices.Motor(devicePath)
            else:
                # default existing motor
                self.defaultMotorDevice = devices.Motor(config.DEVICE_MOTOR)

        self.action_change_motor()
        self.__init_variables()
        self.__init_signals()
        self.__init_ui()
        self.__main()

        # self.layout_horizontal.addStretch(10)

    def __init_variables(self):
        self.ledStatus = led_widget.DeviceLedStatusWidget(self.defaultMotorDevice)
        self.attributeTable = None

        # previous selected step
        self.__last_step = []

        # assign step minimal step size
        config = self._init_motor_step()
        self.step_size.setValue(config[0])

    def __init_ui(self):
        pass

    def __init_signals(self):
        self.connect(self, Qt.SIGNAL("changeMotor(QString)"), self.action_change_motor)
        self.connect(self.motor_position, Qt.SIGNAL("valueChanged()"), self.action_read_motor_position)
        self.connect(self.ledStatus, signals.SIG_DEVICE_STATUS_CHANGED, self.action_enable_controls)
        self.connect(self.ledStatus, signals.SIG_DEVICE_STATUS_ERROR, self.action_device_error)
        self.connect(self.ledStatus, signals.SIG_DEVICE_STATUS_OK, self.action_device_ok)
        self.connect(self.ledStatus, signals.SIG_DEVICE_WORKING, self.read_motor_position_and_set)

        # create special step size for specific motors
        self.step_size.setContextMenuPolicy(Qt.Qt.CustomContextMenu)

        # events
        self.motor_position.leaveEvent = self.action_leave_event

    def __main(self):
        layout = self.layout()
        layout.insertWidget(0, self.ledStatus)
        self.spinboxFilter = default_gui.EventSpinboxFilter()
        self.motor_position.installEventFilter(self.spinboxFilter)

    def _init_motor_step(self):
        """
        Initializes steps for the step control widget
        :return:
        """
        config = None
        for i in range(1, len(STEP_SETTINGS)):
            names = STEP_SETTINGS[i][KEYMS_NAMES]

            for name in names:
                if name.lower() in self.defaultMotorDevice.name.lower():
                    config = STEP_SETTINGS[i]

        if config is None:
            config = STEP_SETTINGS[0]

        config = config[KEYMS_STEPS]
        self.step_size.setRange(0, 2 * max(config))
        self.step_size.setSingleStep(min(config))
        return config

    def action_leave_event(self, event):
        """
        Returns motor positions to current on mouse leaving the position widget
        :param event:
        :return:
        """
        self.action_change_motor()
        event.accept()

    def action_step_menu(self, point):
        """
        Sets the menu for step selection
        :param point:
        :return:
        """

        config = self._init_motor_step()

        format = '%6.5f'
        menu = QtGui.QMenu(self)
        if len(self.__last_step) > 0:
            for value in self.__last_step:
                value = format % value

                while value[-1]=='0':
                    value = value[:-1]
                menu.addAction(value)
            menu.addSeparator()

        for step in config:
            value = format % step

            while value[-1]=='0':
                value = value[:-1]
            menu.addAction(value)

        self.connect(menu, Qt.SIGNAL('triggered (QAction*)'), self.action_step_selected)
        menu.popup(self.step_size.mapToGlobal(point))

    def action_step_selected(self, action):
        """
        Sets selected step size to the item
        :param action: QAction()
        :return:
        """
        self._add_last_step(self.step_size.value())
        value = float(action.text())
        self.step_size.setValue(value)

    def _add_last_step(self, value):
        """
        Controls number of saved points in the steps control context menu
        :param value: float()
        :return:
        """
        self.__last_step.insert(0, value)
        if len(self.__last_step) > 3:
            self.__last_step.pop(-1)
        pass

    def action_show_settings_window(self):
        attributeFilter = ["CcwLimit", "CwLimit", "UnitLimitMax", "UnitLimitMin", "StepBacklash", "PositionEncoder",
                           "SlewRate", "SlewRateMin", "SlewRateMax", "BaseRate", "Conversion",
                           "Acceleration", "StepLimitMin", "StepLimitMax", "UnitBacklash",
                           "SettleTime", "State", "Calibrate"]
        cmdFilter = ["Calibrate", "MoveCCW", "MoveCW", "StopMove", "StartMove"]
        if not self.attributeTable: self.attributeTable = dialogs.MotorAttributeDialog(
            self.defaultMotorDevice.devicePath, self, attributeFilter=attributeFilter, cmdFilter=cmdFilter)

        self.attributeTable.setWindowIcon(self.windowIcon())
        self.attributeTable.show()

    def close_widget(self):
        self._closeAttributeTable()
        return default_gui.DefaultControls.close_widget(self)

    def closeEvent(self, event):
        self._closeAttributeTable()
        return default_gui.DefaultControls.closeEvent(self, event)

    def _closeAttributeTable(self):
        if self.attributeTable is not None:
            try:
                self.attributeTable.close()
            except AttributeError:
                pass

    def action_device_error(self):
        self.stackedWidget.setCurrentIndex(1)

    def action_device_ok(self):
        self.stackedWidget.setCurrentIndex(0)
        self.emit(Qt.SIGNAL("changeMotor(QString)"), self.action_change_motor)

    def action_change_motor_position_plus_double(self):
        """
        motorAlias
        Change position by clicking the right double arrow button
        Position = Position + StepSize * 10
        """
        step = float(self.step_size.value())
        self.action_change_motor()
        position = self.motor_position.value()
        newPosition = position + step * 10
        self.action_set_motor_position(newPosition)
        self.action_change_motor()

    def action_change_motor_position_plus(self):
        """
        Change position by clicking the right arrow button
        Position = Position + StepSize
        """
        step = float(self.step_size.value())
        self.action_change_motor()
        position = self.motor_position.value()
        newPosition = position + step
        self.action_set_motor_position(newPosition)
        self.action_change_motor()

    def action_change_motor_position_minus_double(self):
        """
        Change position by clicking the left double arrow button
        Position = Position - StepSize * 10
        """
        step = float(self.step_size.value())
        self.action_change_motor()
        position = self.motor_position.value()
        newPosition = position - step * 10
        self.action_set_motor_position(newPosition)
        self.action_change_motor()

    def action_change_motor_position_minus(self):
        """
        Change position by clicking the left arrow button
        Position = Position - StepSize
        """
        step = float(self.step_size.value())
        self.action_change_motor()
        position = self.motor_position.value()
        newPosition = position - step
        self.action_set_motor_position(newPosition)
        self.action_change_motor()

    def action_change_motor_position_zero(self):
        """
        Change position by clicking the 0  button
        """
        res = QtGui.QMessageBox.warning(self, 'Position change', 'Do you really want to go to the zero position?',
                                        QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
        if res == QtGui.QMessageBox.Ok:
            position = 0.
            self.action_set_motor_position(position)

    def action_change_motor(self):
        """
        Change actual motor
        """
        self.defaultMotorDevice.__postInit__()
        self.motor_position.setToolTip('User defined limits (%6.4f; %6.4f); Real device position (%6.4f);' % (
            self.defaultMotorDevice.minValue, self.defaultMotorDevice.maxValue, self.defaultMotorDevice.current_value()))

        # redefine minimum and maximum for the motors
        self.check_device_allowed_values([self.motor_position], self.defaultMotorDevice, minimum=-1e6, maximum=1e6)

        actualPosition = float(self.defaultMotorDevice.current_value())
        if actualPosition is not None and isinstance(actualPosition, float):
            self.motor_position.setValue(actualPosition)

    def action_enable_controls(self, flag=True):
        """
        Enable / disable controls
        """
        self.button_stop_all_moves.setEnabled(not flag)
        self.motor_controls.setEnabled(flag)
        if flag:
            self.read_motor_position_and_set()

    def action_change_step(self, step):
        """
        Change current stepSize
        """
        self.motor_position.setSingleStep(step)

    def action_read_motor_position(self):
        """
        Read current motor position from spinbox and change motor position
        """
        position = self.motor_position.value()
        self.action_set_motor_position(position)

    def read_motor_position_and_set(self):
        """
        Get motor position and set the spinbox value - executed on motor change update
        """
        # actualPosition = float(self.defaultMotorDevice.current_value())
        # get new limits
        # self.defaultMotorDevice.__postInit__()
        # self.motor_position.setValue(actualPosition)

        self.action_change_motor()

    def action_stop_motor(self):
        """
        Stop motor movement
        """
        self.defaultMotorDevice.halt()

    def action_set_motor_position(self, position):
        """
        Set motor position, check limitis before
        """
        try:
            # check again limits
            self.defaultMotorDevice.__postInit__()

            # test if we want to go beyond the limit - disabled KG - HPL decision
            # self.validate_device_minmax_value(position, self.defaultMotorDevice)

            self.defaultMotorDevice.move(position, async=True)
            # self.motor_position.setValue(position)
        except:
            self.emit(signals.SIG_SHOW_ERROR, "Motor position", "Motor limits was exceeded")
            self.read_motor_position_and_set()
            return

        # MAIN PROGRAM #################################################################################


if __name__ == '__main__':
    from taurus.qt.qtgui.application import TaurusApplication

    # test if we have polling period - insert one in case of absence
    bfound = False
    for (i, el) in enumerate(sys.argv):
        if "--polling-period" in el:
            bfound = True

    if not bfound:
        sys.argv.append("--taurus-polling-period=250")

    app = TaurusApplication(sys.argv)

    # init widget
    # left = devices.Motor(config.DEVICE_SERVER + "p02/motor/exp.04")
    #right = devices.Motor(config.DEVICE_SERVER + "p02/motor/exp.05")
    #virtualMotor1 = devices.VirtualMotorDistance2D([left, right], "Dx")

    widget = MotorWidget(device=devices.Motor("haspp02oh1:10000/p02/motor/eh2b.42"))

    # connect signal from window "x" button to close the application correctly
    app.connect(app, signals.SIG_ABOUT_QUIT, widget.close_widget)

    # connect signal from keyboard interruption (if widget is closed with ctrl+c from console)
    signal.signal(signal.SIGINT, lambda *args, **kwargs: widget.close())

    # show widget
    widget.show()

    # execute application
    app.exec_()
