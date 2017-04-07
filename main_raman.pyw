import os
import sys

from taurus.qt.qtgui.application import TaurusApplication
from Revolver.gui_raman_window import RamanWindow

from Revolver.common import create_path
from Revolver.config.keys import *
import Revolver.config.config_global as config

FILE = __file__

def prep_app():
    """
    Prepares the qt application + parameters
    @return:
    """
    bfound = False
    for (i, el) in enumerate(sys.argv):
        if "--polling-period" in el:
            bfound = True

    if not bfound:
        sys.argv.append("--taurus-polling-period=250")

    return TaurusApplication(sys.argv)

def prepare_html():
    """
    Updates paths for the html+script
    :return:
    """
    global FILE
    config.HTML[HTML_CALC_PATH] = create_path(FILE, "Revolver", "html", "calculations.html")
    config.HTML[HTML_POS_PATH] = create_path(FILE, "Revolver", "html", "positions.html")

def prep_settints(app):
    """
    Prepares the settings ref. for the application
    @return:
    """
    app.setOrganizationName("Petra-III")
    app.setOrganizationDomain("desy.de")
    app.setApplicationName("P02.2 Offline Raman System")

def main():
    """
    Starts the application
    @return:
    """
    # prepare paths and etc.
    prepare_html()

    # prepare application
    app = prep_app()

    # show main window
    w = RamanWindow()

    app.exec_()

if __name__ == "__main__":
    main()