import sys

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QDesktopWidget, QPushButton, QHBoxLayout, QLabel, QLineEdit, \
    QVBoxLayout, QFileDialog, QDialog, QFormLayout, QDialogButtonBox, QApplication, QDoubleSpinBox


class BlockDialog(QDialog):

    new_block_signal = pyqtSignal(list, list, list, list)

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setModal(True)

        self.vertex_count = 8
        vbox = QVBoxLayout(self)
        form = QFormLayout()
        form.setSpacing(25)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("X"))
        hbox.addWidget(QLabel("Y"))
        hbox.addWidget(QLabel("Z"))
        form.addRow("", hbox)

        self.measure = []
        self.shift = []
        self.cells = []
        self.ratios = []

        self.mhbox = QHBoxLayout()
        self.mhbox.setSpacing(20)

        self.vhbox = QHBoxLayout()
        self.vhbox.setSpacing(20)

        self.chbox = QHBoxLayout()
        self.chbox.setSpacing(20)

        self.rhbox = QHBoxLayout()
        self.rhbox.setSpacing(20)

        for coord in range(3):
            m = QLineEdit()
            m.setValidator(QDoubleValidator(0.0, 999999, 50))
            m.setText("1")
            self.measure.append(m.text().replace(',','.'))
            self.mhbox.addWidget(m)

            v = QLineEdit()
            v.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
            v.setText("0")
            self.shift.append(v.text().replace(',','.'))
            self.vhbox.addWidget(v)

            c = QLineEdit()
            c.setValidator(QIntValidator(0, 999999))
            c.setText("20")
            self.cells.append(c.text())
            self.chbox.addWidget(c)

            r = QLineEdit()
            r.setValidator(QDoubleValidator(0.0, 999999.0, 50))
            r.setText("1")
            self.ratios.append(r.text().replace(',','.'))
            self.rhbox.addWidget(r)

        form.addRow("Measurements", self.mhbox)
        form.addRow("Shift vector", self.vhbox)
        form.addRow("Number of cells", self.chbox)
        form.addRow("Cell expansion ratios", self.rhbox)


        buttonbox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

        vbox.addLayout(form)
        vbox.addWidget(buttonbox)

        self.setFixedSize(550, 350)
        self.center()
        self.setWindowTitle('New block')

    def accept(self):
        self.measure.clear()
        for i in range(0, self.mhbox.count()):
            coord = self.mhbox.itemAt(i).widget().text()
            self.measure.append(coord)

        self.shift.clear()
        for i in range(0, self.vhbox.count()):
            coord = self.vhbox.itemAt(i).widget().text()
            self.shift.append(coord)

        self.cells.clear()
        for i in range(0, self.chbox.count()):
            coord = self.chbox.itemAt(i).widget().text()
            self.cells.append(coord)

        self.ratios.clear()
        for i in range(0, self.rhbox.count()):
            coord = self.rhbox.itemAt(i).widget().text()
            self.ratios.append(coord)

        self.new_block_signal.emit(self.measure, self.shift, self.cells, self.ratios)
        super().accept()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


