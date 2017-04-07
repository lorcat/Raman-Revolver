"""
Dialogs used in widgets
"""

# import from global packages 
from PyQt4 import QtGui, Qt
from PyQt4.QtGui import QPushButton

# Import from local packages
from Revolver.UI.layout_motor_params import Ui_Form
from taurus.qt.qtgui.container import TaurusWidget


from taurus.qt.qtgui.panel import TaurusAttrForm, TaurusForm, TaurusCommandsForm

class DeviceAttributeDialog(QtGui.QDialog, TaurusWidget, Ui_Form):
    
    def __init__(self, devicePath, parent=None, attributeFilter=None, cmdFilter=None):
        # Initialization

        super(DeviceAttributeDialog, self).__init__()

        self.setupUi(self)

        # local function helping with the view filters
        def displayAttrFilter(attribute):
            if attribute.label in attributeFilter:
                return True

        def displayCmdFilter(cmd_info):
            if cmd_info.cmd_name in cmdFilter:
                return True


        self.devicePath = devicePath

        attrform = TaurusAttrForm(self)

        # prepare attr form
        if isinstance(attrform, TaurusAttrForm):
            attrform._form.setWithButtons(False)

            if attributeFilter is not None:


                attrform.setViewFilters([displayAttrFilter])
        elif isinstance(attrform, TaurusForm):
            attrform.setWithButtons(False)

        # prepare commands form
        cmdform = TaurusCommandsForm(self)
        if cmdFilter is not None:
            cmdform.setViewFilters([displayCmdFilter])

        # setting the model
        attrform.setModel(devicePath)
        cmdform.setModel(devicePath)

        # updating the widget
        self.tab_attributes.layout().addWidget(attrform)
        self.tab_commands.layout().addWidget(cmdform)
        
        self.mainAttrForm = attrform
        self.mainCmdForm = cmdform

        self.attr_filter = attributeFilter
        self.cmd_filter = cmdFilter

        self.setWindowTitle("Parameters for the device @ %s" % devicePath)
        

class MotorAttributeDialog(DeviceAttributeDialog):
    
    def __init__(self, devicePath, parent=None, attributeFilter=None, cmdFilter=None):
        super(MotorAttributeDialog, self).__init__(devicePath, parent, attributeFilter=attributeFilter, cmdFilter=cmdFilter)
        
        encoderButton = QPushButton("Encoder")
        self.connect(encoderButton, Qt.SIGNAL("clicked()"), self.openEncoderDialog)

        if isinstance(self.mainAttrForm, TaurusAttrForm):
            self.mainAttrForm.children()[1].children()[2].addButton(encoderButton, 0)
        
    def openEncoderDialog(self):
        attributes = ["State","Position","StepPositionController","StepPositionInternal","StepPosition","EncoderRawPosition",
                      "HomePosition","FlagHomed","EncoderConversion","EncoderRatio","FlagUseEncoderPosition",
                      "FlagClosedLoop","FlagInvertEncoderDirection","CorrectionGain","DeadBand",
                      "SlewRateCorrection","SlipTolerance","WriteRead"]
        encoderAttribute = DeviceAttributeDialog(self.devicePath, self.parent(), attributeFilter=attributes)
        encoderAttribute.exec_()

