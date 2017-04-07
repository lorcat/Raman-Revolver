"""
Motor widget.
Populate motor position to user, which can be changed.
User can also stop all movements of selected motor.
Motor status is signalized by diode.
"""

# import global classes 
from PyQt4 import QtGui
import sys
import signal
 
# Import local classes
from Revolver.classes import devices, signals

from Revolver.UI import layout_stacked_motors_controls

from Revolver import gui_default_widget, gui_motor_controls_widget_advanced

import Revolver.gui_default_controls_widget as default_gui

class StackedMotorControls(layout_stacked_motors_controls.Ui_Form, default_gui.DefaultControls):
    
    def __init__(self, parent=None, motors=None, title=None):
        super(StackedMotorControls, self).__init__()
        default_gui.DefaultControls.__init__(self, parent=parent)
        self.motors = motors
        self.title = title

        self.__init_variables()

        self.__main()

        self.__init_signals()
    
    def __init_variables(self):
        self.setup = {}

        # device paths for expert mode control
        self.__expert_mode_path = []
    
    def __init_signals(self):
        pass
        
    def __main(self):
        if self.motors:
            layout = self.stage_motors.layout()
            for motor in self.motors:
                bdevice = True
                if isinstance(motor, str) or isinstance(motor, unicode):
                    motor_controls = gui_motor_controls_widget_advanced.MotorWidget(devicePath=motor)
                    self.setup[motor] = motor_controls
                elif isinstance(motor, devices.Motor):
                    motor_controls = gui_motor_controls_widget_advanced.MotorWidget(device=motor)
                    self.setup[motor.devicePath] = motor_controls
                else:
                    bdevice = False

                if bdevice:
                    self.insert_widget(motor_controls, layout)
            layout.setRowStretch(layout.rowCount()+1, 50)
        
    def set_motor_controls_enabled(self, motorPath, flag=True):
        try:
            self.setup[motorPath].setEnabled(flag)
        except:
            self.emit(signals.SIG_SHOW_ERROR, "Controller error", "Controller does not exists")
    
# MAIN PROGRAM #################################################################################

if __name__ == '__main__':
    
    # create main window
    app = QtGui.QApplication(sys.argv)

    DEVICE_SERVER = "haspp02oh1.desy.de:10000/"
    
    # init widget
    left = devices.Motor(DEVICE_SERVER + "p02/motor/eh2b.42")
    right = devices.Motor(DEVICE_SERVER + "p02/motor/eh2b.43")

    widget = StackedMotorControls(motors=[left, right])
    
    widget3 = gui_default_widget.DefaultWidget()
    widget3.setLayout(QtGui.QGridLayout())
    widget3.layout().addWidget(widget)
    
    win = gui_default_widget.DefaultMainWindow()
    win.setCentralWidget(widget3)
    
    # connect signal from window "x" button to close the application correctly
    app.connect(app, signals.SIG_ABOUT_QUIT, widget.close_widget)

    # connect signal from keyboard interruption (if widget is closed with ctrl+c from console)
    signal.signal(signal.SIGINT, lambda *args, **kwargs: widget.close())
    
    # show widget
    win.show()
    
    # execute application
    app.exec_()
