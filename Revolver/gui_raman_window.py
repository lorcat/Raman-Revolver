from PyQt4 import QtCore, QtGui

from Revolver.common import Tester
from Revolver.classes import devices
from Revolver.classes.schott_device import getLightControl
from Revolver.gui_stacked_motors_controls_widget import StackedMotorControls

from Revolver.config.keys import *
import Revolver.config.config_global as config

from Revolver.runnables import getPool, DoorRunner, LambdaRunner, PytangoRunner
from Revolver.pytango import getMotorPosition, setMotorPosition

from Revolver.gui_dialog_calibration import CalibrationDialog

from Revolver.UI.layout_raman_window import Ui_MainWindow

from Revolver.gui_diamond_correction import DiamondCorrectionWidget

# fill the information on the devices
P02_DEVICES = dict((x, config.DEVICE_SERVER_P02  + y) for x, y in config.DEVICE_NAMES.iteritems())
devices.DEVICE_NAMES = dict((y, x) for x, y in config.DEVICE_NAMES.iteritems())
devices.DEVICE_PATHS = P02_DEVICES

class RamanWindow(QtGui.QMainWindow, Tester, Ui_MainWindow):

    WINDOW_TITLE = "Offline Raman system"

    # keys to work with for QSettings
    WIN_SIZE = "size"
    WIN_POS = "position"

    # JS template to send result of operation back
    JS_MACRO_TMPL = "ExtQt.processMacroResponse(%DATAOUT%, %DATAINFO%, %DATAERR%);"

    JS_MACRO_SUBSTOUT = "%DATAOUT%"
    JS_MACRO_SUBSTINFO = "%DATAINFO%"
    JS_MACRO_SUBSTERR = "%DATAERR%"

    # templates to look for and substitute motor positions
    JS_MOTX = "%MOTX%"
    JS_MOTY = "%MOTY%"
    JS_MOTZ = "%MOTZ%"

    # key for motors
    MOTORX = "RAMANX"
    MOTORY = "RAMANY"
    MOTORZ = "RAMANZ"
    MOTORFILT = "RAMANFILT"

    STYLE_ON = "QLabel {background-color: #0d0; font-size: 12pt; padding: 5 0 5 0;};"
    STYLE_OFF = "QLabel {background-color: #d00; font-size: 12pt; padding: 5 0 5 0;};"

    # settings for the festo controls
    FESTODEVICE = 'haspllabcl1:10000/llab/ramanoptics/llabcl1.01'
    ATTR_LC = "Valve1"
    ATTR_CC = "Valve2"
    ATTR_NF = "Valve3"
    ATTR_SH = "Valve4"

    FESTO_ON = 1
    FESTO_OFF = 0

    def __init__(self):
        super(RamanWindow, self).__init__()
        Tester.__init__(self)

        self.debug("Initializin main window")

        self.__init_variables()
        self.__init_gui()
        self.__init_events()

        self.readSettings()

        self.actionLightOff()

        self.show()

    def __init_variables(self):
        self.debug("Init variables")

        # motors widget
        self.motors = None

        # widget with diamond correction
        self.diacorr = None

        # tread pool
        self._thread_pool = getPool(parent=self)

    def __init_gui(self):
        self.debug("Initializing gui")

        # create elements
        self.setupUi(self)

        # adding diamond correction widget
        self.addDiamondCorrection()

        # add motor widgets
        self.addMotors()

        # html - for calculations
        self.initializeCalculationsHtml()
        # html for position saving
        self.initializePositionsHtml()

        # window title
        self.setWindowTitle(self.WINDOW_TITLE)

    def __init_events(self):
        self.debug("Initializing qt events for main window")

    def addMotors(self):
        """
        Loading motor names, adding the devices to the gui
        @return:
        """

        motors = [
                P02_DEVICES[self.MOTORX],
                P02_DEVICES[self.MOTORY],
                P02_DEVICES[self.MOTORZ],
                P02_DEVICES[self.MOTORFILT]
            ]

        self.motors = StackedMotorControls(parent=self, motors=motors, title="Microscope Motors")
        self.wdgt_motors.layout().addWidget(self.motors)

    def addDiamondCorrection(self):
        """
        Adding a widget with diamond correction
        @return:
        """
        self.diacorr = DiamondCorrectionWidget(parent=self)
        self.wdgt_diacorr.layout().addWidget(self.diacorr)

    def initializeCalculationsHtml(self):
        """
        Initialize calculations part
        @return:
        """
        fn = config.HTML[HTML_CALC_PATH]
        self.debug("Setting calculations HTML page ({})".format(fn))

        url = QtCore.QUrl()
        url.setPath(fn)

        frame = self.wv_calc.page().mainFrame()
        self.connect(frame, QtCore.SIGNAL("javaScriptWindowObjectCleared()"), self.processReloadCalcHtmlPage)
        self.connect(self.wv_calc, QtCore.SIGNAL("loadFinished (bool)"), self.processReloadCalcHtmlPage)
        self.wv_calc.setUrl(url)

    def initializePositionsHtml(self):
        """
        Initialize calculations part
        @return:
        """
        fn = config.HTML[HTML_POS_PATH]
        self.debug("Setting positions HTML page ({})".format(fn))

        url = QtCore.QUrl()
        url.setPath(fn)

        frame = self.wv_save.page().mainFrame()
        self.connect(frame, QtCore.SIGNAL("javaScriptWindowObjectCleared()"), self.processReloadPosSaveHtmlPage)
        self.connect(self.wv_save, QtCore.SIGNAL("loadFinished (bool)"), self.processReloadPosSaveHtmlPage)
        self.wv_save.setUrl(url)

    @QtCore.pyqtSlot()
    def processReloadCalcHtmlPage(self, *args):
        """
        Processes events on html page reload for indicator page - adds an javascript object
        :return:
        """
        self.wv_calc.page().mainFrame().addToJavaScriptWindowObject("qtWindow", self)

    @QtCore.pyqtSlot()
    def processReloadPosSaveHtmlPage(self, *args):
        """
        Processes events on html page reload for indicator page - adds an javascript object
        :return:
        """
        self.wv_save.page().mainFrame().addToJavaScriptWindowObject("qtWindow", self)

    @QtCore.pyqtSlot()
    def jsTest(self):
        """
        Simple test demonstrating communication of HTML+JS with Qt
        @return:
        """
        QtGui.QMessageBox.information(self, "Greetings from JS", "Test fired by JS script")
        self.info("size and position ({}, {})".format( self.size(), self.pos()))

    def readSettings(self):
        """
        Reads settings from registry
        @return:
        """
        self.debug("Reading settings")
        settings = QtCore.QSettings()

        size = settings.value(self.WIN_SIZE, QtCore.QSize(*config.DEFAULT_WINDOW_SIZE))
        pos = settings.value(self.WIN_POS, QtCore.QPoint(*config.DEFAULT_WINDOW_POS))

        self.move(pos)

        self.resize(size)

        self.settings = settings


    def writeSettings(self):
        """
        Writing settings for position and size
        @return:
        """
        self.debug("Writing settings")

        self.settings.setValue(self.WIN_SIZE, self.size())
        self.settings.setValue(self.WIN_POS, self.pos())

    def closeEvent(self, event):
        """
        Cleanup during the close event
        @param args:
        @param kwargs:
        @return:
        """
        self.debug("Closing the window")

        self.actionLightOff()

        self.writeSettings()
        event.accept()

    @QtCore.pyqtSlot(str)
    def jsRunMacro(self, cmdline):
        """
        Takes the macro parameter from the HTML+JS and run it
        @return:
        """
        self.debug("Tryting to run macro ({})".format(cmdline))

        args = cmdline.split(" ")
        door = args.pop(0)

        # get rid of empty arguments
        tmp_args = []
        for (i, el) in enumerate(args):

            key = self.MOTORX
            if el == self.JS_MOTX:
                pos = getMotorPosition(devices.DEVICE_PATHS[key])
                if self.testFloat(pos):
                    el = "{:.4f}".format(getMotorPosition(devices.DEVICE_PATHS[key]))
                else:
                    return

            key = self.MOTORY
            if el == self.JS_MOTY:
                pos = getMotorPosition(devices.DEVICE_PATHS[key])
                if self.testFloat(pos):
                    el = "{:.4f}".format(getMotorPosition(devices.DEVICE_PATHS[key]))
                else:
                    return

            key = self.MOTORZ
            if el == self.JS_MOTZ:
                pos = getMotorPosition(devices.DEVICE_PATHS[key])
                if self.testFloat(pos):
                    el = "{:.4f}".format(getMotorPosition(devices.DEVICE_PATHS[key]))
                else:
                    return

            if len(el) > 0:
                tmp_args.append(el)

        self.debug("Final command for the door ({}) is ({})".format(door, tmp_args))

        runner = DoorRunner(door, tmp_args, response_func=self.jsResponseMacro)
        self._thread_pool.tryStart(runner)

    @QtCore.pyqtSlot(str)
    def jsResponseMacro(self, *args):
        """
        Takes the response from the macro server and output it fith some filtering
        @return:
        """
        self.debug("Receiving response from the macro server door ({})".format(args))

        # get all - info+error are colored
        output, info, error = args

        if not self.test(output,list) and not self.test(output, tuple):
            output = [output]

        if not self.test(info, list) and not self.test(info, tuple):
            info = [info]

        if not self.test(error, list) and not self.test(error, tuple):
            error = [error]

        tmpl = self.JS_MACRO_TMPL.replace(self.JS_MACRO_SUBSTOUT, str(list(output)))
        self.debug("Template: {}".format(tmpl))
        tmpl = tmpl.replace(self.JS_MACRO_SUBSTINFO, str(list(info)))
        self.debug("Template: {}".format(tmpl))
        tmpl = tmpl.replace(self.JS_MACRO_SUBSTERR, str(list(error)))
        self.debug("Template: {}".format(tmpl))

        self.debug("Executing Javascript: ({});\n".format(tmpl))

        self.wv_save.page().mainFrame().evaluateJavaScript(tmpl)
        self.wv_save.update()

    @QtCore.pyqtSlot()
    def actionLightOff(self):
        """
        Performing a light on action
        @return:
        """
        self.debug("Performing a light on action")

        schott = getLightControl()
        func = lambda v=0: schott.set_light(v)

        runner = LambdaRunner(func)
        self._thread_pool.start(runner)

        self.lb_lightstate.setText("OFF")
        self.lb_lightstate.setStyleSheet(self.STYLE_OFF)

    @QtCore.pyqtSlot()
    def actionLightOn(self):
        """
        Performing a light off action
        @return:
        """
        self.debug("Performing a light off action")

        schott = getLightControl()
        func = lambda v=1: schott.set_light(v)

        runner = LambdaRunner(func)
        self._thread_pool.start(runner)

        self.lb_lightstate.setText("ON")
        self.lb_lightstate.setStyleSheet(self.STYLE_ON)

    @QtCore.pyqtSlot()
    def actionLightSet(self):
        """
        Performing a light set action
        @return:
        """
        pos = self.sliderToLight()
        self.debug("Performing a light set action ({})".format(pos))

        schott = getLightControl()
        func = lambda v=pos: schott.set_light_power(v)

        runner = LambdaRunner(func)
        self._thread_pool.start(runner)

    @QtCore.pyqtSlot()
    def actionPrepCollection(self):
        """
        Performing preparations for data collection
        @return:
        """
        self.debug("Performing preparations for data collection")

        # individial actions for collection
        # switch off the light, remove the light and camera cubes
        self.actionLightOff()
        self.actionLCoff()
        self.actionCCoff()
        self.actionSHoff()

    @QtCore.pyqtSlot()
    def actionPrepObservation(self):
        """
        Performing preparations for observation adjustments
        @return:
        """
        self.debug("Performing preparations for observation adjustments")

        # individial actions for observation
        # switch on the light, move in the light and camera cubes
        self.actionLCon()
        self.actionCCon()
        self.actionLightOn()
        self.actionSHon()

    @QtCore.pyqtSlot()
    def actionPrepAlignment(self):
        """
        Performing preparations for alignment adjustments
        @return:
        """
        self.debug("Performing preparations for alignment adjustments")

        # individial actions for observation
        # switch on the light, move in the light and camera cubes
        self.actionLCon()
        self.actionCCon()
        self.actionLightOn()
        self.actionSHoff()

    def sliderToLight(self):
        """
        Converts the position of the slider into the light
        @return:
        """
        pos = float(self.sld_lightSet.value())

        # conversion factors
        ma, la = 99., 255.

        return int(pos *la / ma)


    @QtCore.pyqtSlot(object)
    def processMenuAction(self, action):
        """
        Processing actions of the main menu
        @param action:
        @return:
        """
        self.debug("Processing menu action ({})".format(action))

        if "calibrate" in str(action.text()).lower():
            dialog = CalibrationDialog(parent=self)
            dialog.exec_()


    def actionLCon(self):
        """
        Inserts the light cube into the optical path (LightCube)
        @return:
        """
        self.debug("Setting LC ON")
        self.setPytangoRunner(self.FESTODEVICE, self.ATTR_LC, self.FESTO_ON)

    def actionLCoff(self):
        """
        Removes the light cube from the optical path (LightCube)
        @return:
        """
        self.debug("Setting LC OFF")
        self.setPytangoRunner(self.FESTODEVICE, self.ATTR_LC, self.FESTO_OFF)

    def actionCCon(self):
        """
        Inserts the light cube into the optical path (Camera)
        @return:
        """
        self.debug("Setting CC ON")
        self.setPytangoRunner(self.FESTODEVICE, self.ATTR_CC, self.FESTO_ON)

    def actionCCoff(self):
        """
        Removes the light cube from the optical path (Camera)
        @return:
        """
        self.debug("Setting LC OFF")
        self.setPytangoRunner(self.FESTODEVICE, self.ATTR_CC, self.FESTO_OFF)

    def actionNFon(self):
        """
        Inserts the notch filter into the optical path
        @return:
        """
        self.debug("Setting NF ON")
        self.setPytangoRunner(self.FESTODEVICE, self.ATTR_NF, self.FESTO_ON)

    def actionNFoff(self):
        """
        Removes the notch filter from the optical path
        @return:
        """
        self.debug("Setting NF OFF")
        self.setPytangoRunner(self.FESTODEVICE, self.ATTR_NF, self.FESTO_OFF)

    def actionSHon(self):
        """
        Inserts the shutter filter into the optical path
        @return:
        """
        self.debug("Setting SH ON")
        self.setPytangoRunner(self.FESTODEVICE, self.ATTR_SH, self.FESTO_ON)

    def actionSHoff(self):
        """
        Removes the shutter filter from the optical path
        @return:
        """
        self.debug("Setting SH OFF")
        self.setPytangoRunner(self.FESTODEVICE, self.ATTR_SH, self.FESTO_OFF)

    def setPytangoRunner(self, device, attr, value):
        """
        Prepares and starts a thread setting pytango values
        @param device:
        @param attr:
        @param value:
        @return:
        """
        runner = PytangoRunner(device, attr, value)
        self._thread_pool.start(runner)