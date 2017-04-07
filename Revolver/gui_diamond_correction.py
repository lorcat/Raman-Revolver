from PyQt4 import QtCore, QtGui

from Revolver.UI.layout_diamond_corr import Ui_Form
from Revolver.common import Tester
from Revolver.classes import devices
from Revolver.pytango import *
from Revolver.runnables import getPool, LambdaRunner


class DiamondCorrectionWidget(QtGui.QWidget, Tester, Ui_Form):
    MOTORX = None
    MOTORX_KEY = "RAMANX"

    # refraction indexes
    NAIR = 1.000293
    NDIAMOND = 2.419

    # position format
    FORMAT="{:6.4}"

    # limit on the diamond thickness
    MAXH_DIAMOND = 4

    # signals
    # updating calculation
    sign_updatecalc = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        Tester.__init__(self)

        # device path
        self.MOTORX = devices.DEVICE_PATHS[self.MOTORX_KEY]

        # thread pool
        self._thread_pool = getPool(parent=self)

        self.debug("Initializing diamond correction widget")
        self.setupUi(self)

        # signal starting the calculation
        self.sign_updatecalc.connect(self.startCalculation)

        # signals from spinboxes to update the calculation
        self.connect(self.dsb_dtip, QtCore.SIGNAL("valueChanged (double)"), self.startCalculation)
        self.connect(self.dsb_bsurface, QtCore.SIGNAL("valueChanged (double)"), self.startCalculation)

    def setPosition(self, wdgt):
        """
        General processing of the focused positions
        @return:
        """
        self.debug("Processing selected position with widget ({})".format(wdgt))
        pos = getMotorPosition(self.MOTORX)

        if self.testFloat(pos):
            wdgt.setValue(pos)
            self.sign_updatecalc.emit()
        else:
            self.error("Motor position is not float ({})".format(str(pos)))

    def actionDiamondTip(self):
        """
        Obtaining information on the position with focused sample
        @return:
        """
        self.debug("Obtaining information on the position with focused sample")
        self.setPosition(self.dsb_dtip)

    def actionDiamondBSurface(self):
        """
        Obtaining information on the position with focused diamond back surface
        @return:
        """
        self.debug("Obtaining information on the position with focused diamond back surface")
        self.setPosition(self.dsb_bsurface)

    def actionMoveToSample(self):
        """
        Moves to sample position
        @return:
        """
        self.debug("Applying diamond correction, moving the motors")

        # recalculate and try to move
        self.startCalculation(bmove=True)

    def startCalculation(self, dummy_pos=0.0, bmove=False):
        """
        Performes the calculation of diamond correction
        @param move: boolean flag controlling if the motor has to be moved after calculation
        @return:
        """
        self.debug("Performing calculation on diamond correction (Movement: {})".format(bmove))

        # tip position
        pos_tip = self.dsb_dtip.value()
        # diamond back surface position
        pos_bs = self.dsb_bsurface.value()

        # corrected position
        pos_sample = pos_bs + abs(pos_bs - pos_tip) * self.NDIAMOND / self.NAIR;
        # diamond thickness
        h_diamond = abs(pos_sample-pos_bs)

        # show the values
        self.le_sample.setText(self.FORMAT.format(pos_sample))
        self.le_diamond.setText(self.FORMAT.format(h_diamond))

        self.info("Calculated parameters: diamond thickness ({:6.4}); sample position (:6.4)".format(pos_sample, h_diamond))

        # move the motors if needed
        if bmove:
            # test if the calculation makes sense
            if h_diamond >= self.MAXH_DIAMOND:
                self.errorMsg("Diamond thickness is suspiciously large. Aborting the movement.")
                return

            # prepare a lambda runner - to set the position
            func1 = lambda dev=self.MOTORX, pos=pos_sample: setMotorPosition(dev, pos)
            runner1 = LambdaRunner(func1)
            self._thread_pool.tryStart(runner1)

            # prepare a lambda runner - to set the position
            func2 = lambda dev=self.MOTORX: waitForMotorState(dev)
            runner2 = LambdaRunner(func2, self.runnerResponse)
            self._thread_pool.tryStart(runner2)

            self.btn_sample.setEnabled(False)


    @QtCore.pyqtSlot(float)
    def prepCalculation(self, value):
        """
        Processes a signal from double type spin boxes and updates the calculation
        @return:
        """
        self.debug("Updating the calculation with user parameters")
        self.startCalculation()

    def errorMsg(self, msg):
        """
        Shows an error message box
        @param msg:
        @return:
        """
        QtGui.QMessageBox.warning(self, "Error", msg)

    def runnerResponse(self):
        """
        Function receiving a response from a function
        @return:
        """
        self.debug("Received a response from a runner")
        self.btn_sample.setEnabled(True)