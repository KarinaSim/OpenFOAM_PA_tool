from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QGroupBox, QHBoxLayout, QComboBox, QLabel, QLineEdit


class TransportPropsForm(QWidget):
     def __init__( self):
        super().__init__()
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignVCenter | Qt.AlignTop)
        hbox = QHBoxLayout()
        hbox.setSpacing(20)
        hbox.addWidget(QLabel("Transport model"))
        self.model = QComboBox()
        self.model.addItems(["Newtonian"])
        hbox.addWidget(self.model)
        gbox = QGroupBox("Properties")
        hbox_props = QHBoxLayout()
        hbox_props.setSpacing(25)
        hbox_props.addWidget(QLabel("Kinematic viscosity (nu)"))
        self.prop_value = QLineEdit("6e-05")
        self.prop_value.setValidator(QDoubleValidator(0.0, 999999.0, 50))
        hbox_props.addWidget(self.prop_value)
        hbox_props.addWidget(QLabel("m2/c"))
        gbox.setLayout(hbox_props)
        vbox.addLayout(hbox)
        vbox.addWidget(gbox)
        self.setLayout(vbox)

     def set_props(self, nu):
        self.prop_value.setText(nu)

     def read_transportprops_GUIdata(self):
        return self.prop_value.text()
