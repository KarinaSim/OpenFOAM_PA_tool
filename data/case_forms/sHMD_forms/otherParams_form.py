from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QHBoxLayout, QComboBox, QLabel, \
    QCheckBox


class OtherParamsForm(QWidget):

    def __init__(self):
        super(OtherParamsForm, self).__init__()

        layout = QVBoxLayout(self)

        gbox_params = QGroupBox()
        layout.addWidget(gbox_params)
        self.params_form = QFormLayout()
        gbox_params.setLayout(self.params_form)

        self.castellatedMesh = QComboBox()
        self.castellatedMesh.addItems(["true", "false"])
        self.params_form.addRow("castellatedMesh", self.castellatedMesh)


        self.addLayers = QComboBox()
        self.addLayers.addItems(["true", "false"])
        self.params_form.addRow("addLayers", self.addLayers)


        self.snap = QComboBox()
        self.snap.addItems(["true", "false"])
        self.params_form.addRow("snap", self.snap)

        self.mergeTolerance = QLineEdit("1e-6")
        self.mergeTolerance.setValidator(QDoubleValidator(0.0, 999999.0, 50))
        self.params_form.addRow("mergeTolerance", self.mergeTolerance)

        self.writeFlags_hbox = QHBoxLayout()
        self.scalarLevels = QCheckBox("scalarLevels")
        self.scalarLevels.setChecked(True)
        self.layerSets = QCheckBox("layerSets")
        self.layerSets.setChecked(True)
        self.layerFields = QCheckBox("layerFields")
        self.layerFields.setChecked(True)

        self.writeFlags_hbox.addWidget(self.scalarLevels)
        self.writeFlags_hbox.addWidget(self.layerSets)
        self.writeFlags_hbox.addWidget(self.layerFields)
        self.params_form.addRow("writeFlags", self.writeFlags_hbox)



    def set_params(self, otherParams):
        params, writeFlags = otherParams
        self.mergeTolerance.setText(params[3][1])
        for row in range(0, 3):
            self.params_form.itemAt(row, 1).widget().setCurrentText(params[row][1])

        for i in range(0, len(writeFlags)):
            item = self.writeFlags_hbox.itemAt(i).widget()
            item.setText(writeFlags[i][0])
            if writeFlags[i][1] == "true":
                item.setChecked(True)
            else:
                item.setChecked(False)


    def read_otherParams_GUIdata(self):
        params = []
        for row in range(0, 4):
            label = self.params_form.itemAt(row, 0).widget().text()
            value = self.params_form.itemAt(row, 1).widget()
            if isinstance(value, QComboBox):
                value = value.currentText()
            else:
                value = value.text()
            params.append([label, value])

        writeFlags = []
        for i in range(0, self.writeFlags_hbox.count()):
            item = self.writeFlags_hbox.itemAt(i).widget()
            if item.isChecked():
                writeFlags.append([item.text(), "true"])
            else:
                writeFlags.append([item.text(), "false"])


        return [params, writeFlags]
