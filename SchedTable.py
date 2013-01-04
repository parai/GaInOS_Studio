# -*- coding: utf-8 -*-

"""
Module implementing ScheduleTable.
"""

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature

from Ui_SchedTable import Ui_ScheduleTable

class ScheduleTable(QDialog, Ui_ScheduleTable):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
    
    @pyqtSignature("QString")
    def on_cmbxSchedTblSycnStrategy_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
