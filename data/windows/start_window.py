#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QDesktopWidget, QVBoxLayout, \
    QLabel, QGroupBox

from data.windows.main_window import MainWindow
from data.windows.new_case_dwin import NewCaseDialog
from data.windows.open_case_dwin import OpenCaseDialog


class StartWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

       vbox = QVBoxLayout()
       vbox.setSpacing(5)
       vbox.addWidget(QLabel("OpenFOAM_PA_tool"), alignment=Qt.AlignHCenter)
       new_case_btn = QPushButton('New case', self)
       new_case_btn.setFixedSize(110, 70)
       new_case_btn.clicked.connect(self.create_case_dialog)
       open_case_btn = QPushButton('Open case', self)
       open_case_btn.setFixedSize(110, 70)
       open_case_btn.clicked.connect(self.open_case_dialog)

       gbox = QGroupBox()
       gbox.setFixedSize(280, 200)
       vbox_btn = QVBoxLayout()
       vbox_btn.setSpacing(25)
       vbox_btn.setAlignment(Qt.AlignCenter)
       vbox_btn.addWidget(new_case_btn)
       vbox_btn.addWidget(open_case_btn)
       gbox.setLayout(vbox_btn)
       vbox.addWidget(gbox, alignment=Qt.AlignHCenter)
       self.setLayout(vbox)

       self.setFixedSize(550, 350)
       self.center()
       self.setWindowTitle('OpenFOAM_PA_tool')

    def create_case_dialog(self):
        self.new_case_win = NewCaseDialog()
        self.new_case_win.new_case_dialog_signal.connect(self.new_case_dialog_signal_handler)
        self.new_case_win.show()

    def new_case_dialog_signal_handler(self, case_dirname):

        self.main_window = MainWindow("new", case_dirname)
        self.main_window.show()
        self.close()

    def open_case_dialog(self):
        self.open_case_win = OpenCaseDialog()
        self.open_case_win.open_case_dialog_signal.connect(self.open_case_dialog_signal_handler)
        self.open_case_win.show()

    def open_case_dialog_signal_handler(self, case_dirname):
        self.main_window = MainWindow("open", case_dirname)
        self.main_window.show()
        self.close()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

