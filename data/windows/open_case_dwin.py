import re

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDesktopWidget, QFileDialog, QDialogButtonBox, QPushButton, \
    QLineEdit, QHBoxLayout, QLabel, QFormLayout, QVBoxLayout, QDialog, QListWidget
from pymongo import MongoClient


class OpenCaseDialog(QDialog):

    open_case_dialog_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setModal(True)


        client = MongoClient()
        db = client.OpenFOAM_cases
        self.collections = db.collection_names()

        self.list = QListWidget()
        self.list.addItems(self.collections)


        buttonbox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

        vbox = QVBoxLayout()
        vbox.addWidget(self.list)
        vbox.addWidget(buttonbox)
        self.setLayout(vbox)

        self.setFixedSize(550, 350)
        self.center()
        self.setWindowTitle('Open case')

    def set_directory(self):
        dir = QFileDialog.getExistingDirectory(self,"Choose case")
        self.case_dir.setText(dir)

    def accept(self):
        current_case = self.list.currentItem().text()
        self.open_case_dialog_signal.emit(current_case)
        super().accept()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
