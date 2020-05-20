from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QDesktopWidget, QPushButton, QHBoxLayout, QLabel, QLineEdit, \
    QVBoxLayout, QFileDialog, QDialog, QFormLayout, QDialogButtonBox, QApplication, QDoubleSpinBox, QComboBox


class SurfaceDialog(QDialog):

    new_surface_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setModal(True)

        vbox = QVBoxLayout(self)
        form = QFormLayout()
        form.setSpacing(25)

        self.name = QLineEdit()

        form.addRow("Name", self.name)


        buttonbox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

        vbox.addLayout(form)
        vbox.addWidget(buttonbox)

        self.setFixedSize(550, 350)
        self.center()
        self.setWindowTitle('New surface')

    def accept(self):

        self.new_surface_signal.emit(self.name.text())
        super().accept()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

