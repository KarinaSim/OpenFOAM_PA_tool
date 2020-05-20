from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QHBoxLayout, QComboBox, QLabel


class MeshQControlsForm(QWidget):

    def __init__(self):
        super(MeshQControlsForm, self).__init__()

        layout = QVBoxLayout(self)

        gbox_params = QGroupBox()
        layout.addWidget(gbox_params)
        self.params_form = QFormLayout()
        gbox_params.setLayout(self.params_form)

        self.params_form.addRow("#include", QLabel('"meshQualityDict"'))

        self.nSmoothScale = QLineEdit("4")
        self.nSmoothScale.setValidator(QIntValidator(0, 999999))
        self.params_form.addRow("nSmoothScale", self.nSmoothScale)


        self.errorReduction = QLineEdit()
        self.errorReduction.setValidator(QDoubleValidator(0.0, 999999.0, 50))
        self.errorReduction.setText("0.75")
        self.params_form.addRow("errorReduction", self.errorReduction)


        relaxed_hbox = QHBoxLayout()
        self.maxNonOrtho = QLineEdit("75")
        self.maxNonOrtho.setValidator(QIntValidator(0, 999999))
        relaxed_hbox.addWidget(QLabel("maxNonOrtho"))
        relaxed_hbox.addWidget(self.maxNonOrtho)
        self.params_form.addRow("relaxed:", relaxed_hbox)


    def set_params(self, meshQC):
        params, relaxed = meshQC
        self.nSmoothScale.setText(params[1][1])
        self.errorReduction.setText(params[2][1])
        self.maxNonOrtho.setText(relaxed)



    def read_meshQC_GUIdata(self):
        params = []
        for row in range(0, 3):
            label = self.params_form.itemAt(row, 0).widget().text()
            value = self.params_form.itemAt(row, 1).widget().text()
            params.append([label, value])

        label = "maxNonOrtho"
        value = self.maxNonOrtho.text()

        return [params, [label, value]]

