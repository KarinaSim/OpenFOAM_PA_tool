from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QHBoxLayout, QComboBox


class SnapControlsForm(QWidget):

    def __init__(self):
        super(SnapControlsForm, self).__init__()

        layout = QVBoxLayout(self)

        gbox_params = QGroupBox()
        layout.addWidget(gbox_params)
        self.params_form = QFormLayout()
        gbox_params.setLayout(self.params_form)

        self.nSmoothPatch = QLineEdit("3")
        self.nSmoothPatch.setValidator(QIntValidator(0, 999999))
        self.params_form.addRow("nSmoothPatch", self.nSmoothPatch)


        self.tolerance = QLineEdit()
        self.tolerance.setValidator(QDoubleValidator(0.0, 999999.0, 50))
        self.tolerance.setText("1.0")
        self.params_form.addRow("tolerance", self.tolerance)


        self.nSolveIter = QLineEdit("300")
        self.nSolveIter.setValidator(QIntValidator(0, 999999))
        self.params_form.addRow("nSolveIter", self.nSolveIter)


        self.nRelaxIter = QLineEdit("5")
        self.nRelaxIter.setValidator(QIntValidator(0, 999999))
        self.params_form.addRow("nRelaxIter", self.nRelaxIter)


        self.nFeatureSnapIter = QLineEdit("10")
        self.nFeatureSnapIter.setValidator(QIntValidator(0, 999999))
        self.params_form.addRow("nFeatureSnapIter", self.nFeatureSnapIter)


        self.implicitFeatureSnap = QComboBox()
        self.implicitFeatureSnap.addItems(["false", "true"])
        self.params_form.addRow("implicitFeatureSnap", self.implicitFeatureSnap)


        self.explicitFeatureSnap = QComboBox()
        self.explicitFeatureSnap.addItems(["true", "false"])
        self.params_form.addRow("explicitFeatureSnap", self.explicitFeatureSnap)


        self.multiRegionFeatureSnap = QComboBox()
        self.multiRegionFeatureSnap.addItems(["true", "false"])
        self.params_form.addRow("multiRegionFeatureSnap", self.multiRegionFeatureSnap)


    def set_params(self, snapC):
        count = len(snapC)
        for row in range(0, 5):
            self.params_form.itemAt(row, 1).widget().setText(snapC[row][1])
        for row in range(5, count):
            self.params_form.itemAt(row, 1).widget().setCurrentText(snapC[row][1])




    def read_snapC_GUIdata(self):
        params = []
        for row in range(0, self.params_form.rowCount()):
            label = self.params_form.itemAt(row, 0).widget().text()
            value = self.params_form.itemAt(row, 1).widget()
            if isinstance(value, QComboBox):
                value = value.currentText()
            else:
                value = value.text()
            params.append([label, value])
        return params
