import PyTango
import time

from Revolver.common import Tester

def getMotorPosition(device_path):
    """
    Returns position from the motor or None (exception)
    @param self:
    @param device_path:
    @return:
    """
    res = None

    t = Tester()

    try:
        # accesing the Tango device and reading its value
        d = PyTango.DeviceProxy(device_path)
        d.ping()

        state = d.state()

        if state == PyTango.DevState.FAULT:
            raise PyTango.DevFailed

        # same as d.read_attribute("position").value
        res = d.position
        t.debug("Position of the motor ({}:{})".format(device_path, res))

    except (PyTango.DevFailed, AttributeError) as e:
        t.error("Error while reading motor position ({})".format(device_path))

    return res


def setMotorPosition(device_path, pos):
    """
    Tries to sets the motor position in asych. mode, stops the motor movement if needed
    @param self:
    @param device_path:
    @return:
    """
    res = None

    t = Tester()

    try:
        # accesing the Tango device and reading its value
        d = PyTango.DeviceProxy(device_path)
        res = d.state()

        d.command_inout("StopMove")

        waitForMotorState(device_path, time_step=50.)

        # same as d.read_attribute("position").value
        d.write_attribute_asynch("position", pos)
    except (PyTango.DevFailed, AttributeError) as e:
        t.error("Error while writing motor position ({})".format(device_path))

    return res

def waitForMotorState(device_path, state=PyTango.DevState.ON, time_step=200., timeout = 3000.):
    """
    Waits for a pytango device to change state for state with time_step (ms) and timeout (ms)
    @param self:
    @param device_path:
    @return:
    """
    res = None

    t = Tester()

    try:
        # accesing the Tango device and reading its value
        d = PyTango.DeviceProxy(device_path)
        res = d.state()

        time_start = time.time()
        time_finish = time.time()
        while(res!=state):
            time.sleep(time_step/1000.)

            res = d.state()

            time_finish = time.time()
            if time_finish-time_start > timeout:
                t.error("Timeout on waiting for motor to return to ({})".format(state))
                break
            t.debug("Motor state is ({})".format(res))

    except (PyTango.DevFailed, AttributeError) as e:
        t.error("Error while waiting for the motor position ({})".format(device_path))
    return res