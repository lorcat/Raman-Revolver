"""
Created on Oct 3, 2013

@author: Martin Domaracky
@author: Konstantin Glazyrin

Device wrappers
"""

# import from global packages 
import collections
import logging
from threading import Thread
from time import sleep

from PyTango import DeviceProxy, DevState, DevFailed, Database
# Import from local packages
from Revolver.classes import threads
from Revolver.config import config_global as config

# global variables definitions
stopDevices = False
runningDevices = set()

DEVICE_NAMES = {}
DEVICE_PATHS = {}

def getSubDevice(filter):
        exportedDevices = dict()
        db = Database()
        eDevices = db.get_device_exported(filter).value_string
        for eDevice in eDevices:
            sd = db.get_device_property(eDevice, "__SubDevices")["__SubDevices"]
            for s in sd:
                exportedDevices[s] = eDevice
        return exportedDevices
        
SUB_MOTOR_DEVICES = getSubDevice("*motor*")

def halt_all_running_devices():
    """
    Halt all running devices from current widget / application
    """
    logging.warn("Stopping all running registered devices")
    global stopDevices
    global runningDevices
    stopDevices = True
    if runningDevices:
        for device in runningDevices:
            device.halt()
    stopDevices = False
    runningDevices = set()

def get_running_device(devicePath):
    global stopDevices
    if runningDevices:
        for device in runningDevices:
            if device.devicePath == devicePath:
                return device

def get_all_running_devices(devicePath):
    deviceList = []
    if runningDevices:
        for device in runningDevices:
            if device.devicePath == devicePath:
                deviceList.append(device)
    return deviceList

class TangoDevice(object):
    """
    Wrapper for basic Tango device.
    It provides registering device, halting device and executing commands
    """
    POLL_STATE_TIME = 0.5
    TEST_MODE = False
    
    def __init__(self, devicePath=None):
        """
        Class constructor
        @type devicePath: String
        """
        self.devicePath = devicePath
        self.maxValue = False
        self.minValue = False
        self.name = "Generic device"
        self.output = {}
        self.profiling = False
        self.deviceError = False
        self.defaultClass = self.__class__

        # state change marker
        self._bstate_changed = False
        self.old_state = None

        self.__thread = None
        
        try:
            self.__device_init()
        except:
            logging.error(str("Device %s could not be connected" % self.devicePath))
            self.name = self.devicePath
            if config.DEVICE_ALLOW_RETRY:
                self._retry_device()
                #raise Exception(str("Device %s could not be connected" % self.devicePath))
                # logging.error(str("Device %s could not be connected" % self.devicePath))
                #else: 
                
                #raise Exception(str("Device %s could not be connected" % self.devicePath))

    def __postInit__(self):
        pass
    
    def __device_init(self):
        self.device = DeviceProxy(self.devicePath)
        info = self.device.import_info()
        self.name = info.name

        if(self.name in DEVICE_NAMES):
            self.name = DEVICE_NAMES[self.name]

        self.deviceError = False
        self.__postInit__()
                
    def _retry_device(self, callback=None):
        self.deviceError = True
        thread = Thread(target=self.__retry_routine, args=([callback]))
        threads.add_thread(thread)
        thread.start()
        self.__class__ = DummyDevice
    
    def __retry_routine(self, callback):
        retrySleep = [True]
        while(retrySleep[0] and threads.THREAD_KEEP_ALIVE):
            try:
                DeviceProxy(self.devicePath).state()
                logging.error("Device online: %s" % (self.devicePath) )
                retrySleep = [False]
            except:
                logging.error("Device offline, retrying: %s" % (self.devicePath) )
            threads.thread_sleep(config.DEVICE_RETRY_INTERVAL, sleepFlags=retrySleep)
        if threads.THREAD_KEEP_ALIVE == True:
            self.__class__ = self.defaultClass
            self.__device_init()
            if callback: callback()
        return True        
    
    def isDeviceError(self):
        return self.deviceError
        
    def halt(self, callBack=None):
        """
        Stop device
        """
        pass
    
    def running_remove(self, *args):
        """
        Remove device from all running devices set
        """
        try:
            if(not stopDevices):
                runningDevices.remove(self)
        except: pass
    
    def running_add(self):
        """
        Add device to all runing devices set
        """
        global runningDevices
        runningDevices.add(self)
    
    def is_connected(self):
        """
        Return true if device is connected
        @rtype: bool
        """
        if self.device is None: return False
        else: return True
    
    def read_attributes(self, attributes):
        try:
            return self.device.read_attributes(attributes)
        except:
            logging.error("Device read attribute error: retrying device")
            if not config.DEVICE_ALLOW_RETRY: 
                raise Exception(str("Device %s could not be connected" % self.devicePath))
            else:
                self._retry_device()
                return self.read_attributes(attributes)
    
    def read_attribute(self, attribute):
        try:
            return self.device.read_attribute(attribute)
        except:
            if not config.DEVICE_ALLOW_RETRY: 
                raise Exception(str("Device %s could not be connected" % self.devicePath))
            else:
                self._retry_device()
                return self.read_attribute(attribute)
    
    def write_attributes(self, attributes):
        """
        Write attribute to device
        @type attributes: list
        @rtype: String
        """
        res = None
        if self.device:
            for attribute in attributes:
                logging.info("Attribute: %s wrote on device: %s", attribute[0], self.devicePath)

            try:
                self.device.state()
                res = self.device.write_attributes(attributes)
            except (DevFailed, AttributeError) as e:
                pass
        return res
    
    def write_attributes_async(self, attributes, callback=None):
        res = None
        if self.device:
            for attribute in attributes:
                logging.info("Attribute: %s wrote on device: %s", attribute[0], self.devicePath)

            try:
                self.device.state()
                res = self.device.write_attributes_asynch(attributes, callback)
            except (DevFailed, AttributeError) as e:
                pass
        return res
        
    def execute_command(self, commandName, commandParam=None):
        """
        Execute command on device
        @type commandName: String
        @type commandParam: String
        @rtype: String
        """
        try:
            if self.device:
                return self.device.command_inout(commandName, commandParam)
        except:
            if not config.DEVICE_ALLOW_RETRY: 
                raise Exception(str("Device %s could not be connected" % self.devicePath))
            else: 
                self._retry_device()
                return self.execute_command(commandName, commandParam)
            
        
    def wait_for_state(self, state, callback=None):
        """
        Wait for state
        @type state: DevState.state
        """
        if self.device:
            while (self.device.state() == state): sleep (self.POLL_STATE_TIME)
            if not (callback is None): callback(self)
    
    def wait_seconds(self, duration=1):
        """
        Wait for a time duration
        @type duration: float if not config.DEVICE_ALLOW_RETRY: 
                raise Exception(str("Device %s could not be connected" % self.devicePath))
            else: 
                self._retry_device()
                return self.execute_command(commandName, commandParam)
        """
        if self.device:
            sleep(duration)
    
    def poll(self, commandName, duration=0.1, commandResult = True, callback=None, commandParam=None):
        """
        Poll device with command
        @type commandName: String
        @type duration: float
        @type callback: fun
        @type commandParam: String  
        """
        while (self.execute_command(commandName, commandParam) == commandResult and threads.THREAD_KEEP_ALIVE):
            self.wait_seconds(duration)
        if not (callback is None): callback(self)

    def poll_attribute(self, attrName, duration=0.1, attributeResult = True, callback=None, commandParam=None):
        """
        Poll device with command
        @type attrName: String
        @type duration: float
        @type callback: fun
        @type commandParam: String
        """
        while (self.read_attribute(attrName).value == attributeResult and threads.THREAD_KEEP_ALIVE):
            self.wait_seconds(duration)
        if not (callback is None): callback(self)
        
    def check_idle(self):
        """
        Check if device id idle
        """
        pass

    def is_idle(self):
        """
        Return True if is idle, False if not and None if unknown 
        """
        return None
    
    def start_profiling(self):
        if self.profiling: return False
        self.profiling = True
        logging.info("Profiling of device %s started" % self.devicePath)
        return True
    
    def stop_profiling(self):
        self.profiling = False
        self.cleanup_thread()
    
    def current_value(self, value):
        return self.read_attribute(value).value
        
    def __profiling_routine(self):
        pass

    @property
    def thread(self):
        return self.__thread

    def start_external_profiling(self, func):
        """
        Starts profiling with an external function
        """
        self.profiling = True

        if self.__thread is None:
            thread = threads.threading.Thread(target=func, args=([self]))
            threads.add_thread(thread)
            thread.start()

            self.__thread = thread

    def cleanup_thread(self):
        if self.__thread is not None:
            self.profiling = False
            threads.join_thread(self.__thread)
            self.__thread = None

    def state(self):
        """
        Overload of the state function to keep track of old states
        :return:
        """
        state = None
        try:
            state = DeviceProxy(self.devicePath).state()

            self._bstate_changed = False
            if state != self.old_state:
                self.old_state = state
                self._bstate_changed = True
        except DevFailed:
            pass
        return state

    def is_state_changed(self):
        return self._bstate_changed

class DummyDevice(object):
    """
    Wrapper for basic Tango device.
    It provides registering device, halting device and executing commands
    """
    
    TEST_MODE = False
    
    def __init__(self, devicePath):
        """
        Class constructor
        @type devicePath: String
        """
        return
    
    def __device_init(self):
        return False
                
    def _retry_device(self):
        return False
    
    def isDeviceError(self):
        return True    
        
    def halt(self, callBack=None):
        """
        Stop device
        """
        return False
    
    def running_remove(self, *args):
        """
        Remove device from all running devices set
        """
        return False
    
    def running_add(self):
        """
        Add device to all runing devices set
        """
        return False
    
    def is_connected(self):
        """
        Return true if device is connected
        @rtype: bool
        """
        return False
    
    def read_attributes(self, attributes):
        output = []
        for attribute in attributes:
            struct = collections.namedtuple(attribute, "value")
            struct.value = 0 
            output.append(struct)
        return output
    
    def read_attribute(self, attribute):
        struct = collections.namedtuple("struct", "value")
        struct.value = 0
        return struct
    
    def write_attributes(self, attributes):
        return False
    
    def write_attributes_async(self, attributes, callback=None):
        return False
        
    def execute_command(self, commandName, commandParam=None):
        return False
        
    def wait_for_state(self, state, callback=None):
        return False
    
    def wait_seconds(self, duration=1):
        return False
    
    def poll(self, commandName, duration=0.1, callback=None, commandParam=None):
        return False
        
    def check_idle(self):
        return False

    def is_idle(self):
        return False
    
    def start_profiling(self):
        return False
    
    def stop_profiling(self):
        return False
    
    def current_value(self, *args):
        return False
        
    def __profiling_routine(self):
        return False
    
    def get_value(self):
        return 0

        
class Motor(TangoDevice):
    """
    Class that define motor device
    """

    def __init__(self, devicePath=None):
        """
        Class constructor
        @type devicePath: String
        """
        super(Motor, self).__init__(devicePath)

    def __postInit__(self):
        self.maxValue = self.read_attribute("UnitLimitMax").value
        self.minValue = self.read_attribute("UnitLimitMin").value

    def __moved__(self):
        """
        This method is automatically called after motor stops
        """
        self.running_remove()
        self.__postInit__()
        position = self.read_attribute("Position").value
        logging.info("Motor: %s changed position to: %.5f", self.devicePath, position)

    def is_idle(self):
        try:
            if self.device.state() == DevState.MOVING:
                return False
            else:
                return True
        except:
            return None

    def check_idle(self):
        """
        Check if motor is not moving.
        If it's moving raise exception.
        """
        if self.device.state() == DevState.MOVING:
            raise Exception("Motor is moving")

    def halt(self, callBack=None):
        """
        Reimplement TangoDevice.halt
        Stop all motor motions if motor is moving
        """
        # if self.execute_command("CheckMove") == True:
        self.execute_command("StopMove")
        logging.warn("Motor %s halted", self.devicePath)
        if callBack: callBack()

    def move(self, position, callback=None, async=False):
        """
        Move motor to specified position
        @type position: float
        @type callback: fun
        """
        self.check_idle()
        attributes = [("Position", position)]
        if not async:
            self.write_attributes(attributes)
            self.running_add()
        else:
            self.write_attributes_async(attributes, callback)
            self.running_add()

    def current_value(self, value="Position"):
        return TangoDevice.current_value(self, value)

        
class Register(TangoDevice):
    """
    Class that define arbitrary register device with ON and OFF states
    """

    def __init__(self, devicePath=None, config=None):
        """
        Class constructor
        @type devicePath: String
        @type config: dict
        """
        super(Register, self).__init__(devicePath)
        self.config = config

    def halt(self):
        """if self.profiling: return
        do nothing
        """
        pass

    def put_in(self):
        """
        Set Register to ON state
        """
        attr = self.get_config_value("ATTRIBUTE", "value")

        on =  self.get_config_value("ON", 1)

        self.write_attributes([(attr, on)])
        self.running_add()
        logging.info("Setting register (%s/%s) to value (%s)" % (self.name, attr, str(on)))

    def put_out(self):
        """
        Set Register to OFF state
        """
        attr = self.get_config_value("ATTRIBUTE", "value")

        off =  self.get_config_value("OFF", 0)

        self.write_attributes([(attr, off)])
        self.running_remove()

        logging.info("Setting register (%s/%s) to value (%s)" % (self.name, attr, str(off)))

    def get_value(self):
        attr = self.get_config_value("ATTRIBUTE", "value")
        value = self.read_attribute(attr).value
        return self.read_attribute(attr).value

    def is_on(self):
        value = self.get_value()

        on = self.get_config_value("ON", 1)

        return on==value

    def report_configuration_error(self, error, key):
        logging.error("Register (%s) configuration error %s - (%s)" % (self.name, str(error), key))

    def get_config_value(self, key=None, default=None):
        value = default
        try:
            value = self.config[key]
        except KeyError, e:
            self.report_configuration_error(e, key)
        except AttributeError, e:
            self.report_configuration_error(e, key)

        return value

class SardanaDoor(TangoDevice):
    def __init__(self, devicePath=None):
        """
        Class constructor
        @type devicePath: String
        """
        super(SardanaDoor, self).__init__(devicePath)

        self.old_state = None
        self._bstate_changed = False

    def __postInit__(self):
        pass

    def __moved__(self):
        """
        This method is automatically called after motor stops
        """
        self.running_remove()
        self.__postInit__()
        position = self.read_attribute("Position").value
        logging.info("Motor: %s changed position to: %.5f", self.devicePath, position)

    def is_idle(self):
        try:
            state = self.device.state()
            if state == DevState.MOVING or DevState.RUNNING:
                return False
            else:
                return True
        except:
            return None

    def check_idle(self):
        """
        Check if motor is not moving.
        If it's moving raise exception.
        """
        state = self.device.state()
        if state == DevState.MOVING or state == DevState.RUNNING:
            raise Exception("Motor is moving")

    def halt(self, callBack=None):
        """
        Reimplement TangoDevice.halt
        Stop all motor motions if motor is moving
        """
        # if self.execute_command("CheckMove") == True:
        self.execute_command("StopMacro")
