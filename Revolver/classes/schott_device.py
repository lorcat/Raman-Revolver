import sys
import socket

"""
Fast dedicated SCHOTT light control library
"""

SCHOTT = None

def getLightControl():
    global SCHOTT

    if SCHOTT is None:
        SCHOTT = SchottLightControl()

    return SCHOTT

class SchottLightControl(object):
    """
    Set of functions dedicated to the light control
    """

    param_def = []

    HOST = 'haspllabramanlight.desy.de' # 192.168.57.243
    PORT = 50811

    # commands for the socket
    # setting commands
    SET_LIGHT_FORMAT = "&l%i"
    SET_INTENSITY_FORMAT = "&i%02x"

    # inquiring commands
    GET_LIGHT_FORMAT = "%l?"
    GET_INTENSITY_FORMAT = "%i?"
    GET_TEMPERATURE_FORMAT = "%ct?"

    def prep_socket(self):
        """
        sets up the connection to the device
        :return:
        """
        s = None

        # IPV6 + IPV4 example from python tutorials
        for res in socket.getaddrinfo(self.HOST, self.PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
                s.settimeout(3)
            except socket.error as msg:
                #self.error(msg)
                s = None
                continue
            try:
                s.connect(sa)
            except socket.error as msg:
                #self.error(msg)
                s.close()
                s = None
                continue
            break
        return s

    def socket_write(self, cmd):
        """
        Prepares a socket and writes the values
        :param cmd:
        :return:
        """
        res = False

        s = self.prep_socket()
        if s is not None:
            s.sendall(cmd)
            test = s.recv(1024)
            res = True
            s.close()
        return res

    def socket_read(self, cmd):
        """
        Prepares a socket, writes the command to the stream and returns a result
        :param cmd:
        :return:
        """
        res = None

        s = self.prep_socket()
        if s is not None:
            s.sendall(cmd)
            res = s.recv(1024)
            s.close()
        return res

    def set_light(self, bstate = 1):
        """
        Sets the light status ON/OFF
        :return:
        """
        state = int(bstate)
        cmd = self.SET_LIGHT_FORMAT % state
        #self.debug("Setting light state to (%s) with command (%s)" % (state, cmd))
        self.socket_write(cmd)


    def set_light_power(self, value):
        """
        Sets the value for the light
        :param value:
        :return:
        """
        cmd = self.SET_INTENSITY_FORMAT % value
        #self.debug("Setting light power to (%i) with command (%s)" % (value, cmd))
        self.socket_write(cmd)

    def get_light_power(self):
        """
        Returns the value for the light intensity
        :return:
        """
        cmd = self.GET_INTENSITY_FORMAT
        #self.info("Current light power is (%s)" % self.socket_read(cmd))

    def get_light_state(self):
        """
        Returns the value for the light state
        :return:
        """
        cmd = self.GET_LIGHT_FORMAT
        #self.info("Current light state is (%s)" % self.socket_read(cmd))

    def get_light_temperature(self):
        """
        Returns the value for the light
        :return:
        """
        cmd = self.GET_TEMPERATURE_FORMAT
        #self.info("Current light temperature is (%s)" % self.socket_read(cmd))


if __name__ == "__main__":
    from time import sleep

    delay = 0.5

    for i in range(10):
        print("Seq. ({})".format(i))
        schott = getLightControl()

        schott.set_light(i%2)

        sleep(delay)