from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QGroupBox, QHBoxLayout, QComboBox, QLabel, QLineEdit


class TurbulencePropsForm(QWidget):
     def __init__( self):
        super().__init__()
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignVCenter | Qt.AlignTop)

        self.form = QFormLayout()
        self.form.setSpacing(20)


        self.simulationType = QComboBox()
        self.simulationType.addItems(["laminar"])
        self.form.addRow("simulationType", self.simulationType)

        self.RASModel = QComboBox()
        self.RASModel.addItems(["laminar"])
        self.form.addRow("RASModel", self.RASModel)

        self.turbulence = QComboBox()
        self.turbulence.addItems(["off", "on"])
        self.form.addRow("turbulence", self.turbulence)

        self.printCoeffs = QComboBox()
        self.printCoeffs.addItems(["off", "on"])
        self.form.addRow("printCoeffs", self.printCoeffs)

        gbox = QGroupBox()

        gbox.setLayout(self.form)
        vbox.addWidget(gbox)
        self.setLayout(vbox)


     def set_props(self, props):
        count = len(props)
        for row in range(0, count):
            self.form.itemAt(row, 1).widget().setCurrentText(props[row][1])



     def read_turbulenceprops_GUIdata(self):
        props = []
        for row in range(0, self.form.rowCount()):
            label = self.form.itemAt(row, 0).widget().text()
            value = self.form.itemAt(row, 1).widget().currentText()
            props.append([label, value])

        return props
