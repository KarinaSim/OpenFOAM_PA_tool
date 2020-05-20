from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QHBoxLayout, QComboBox


class AddLayersControlsForm(QWidget):

    def __init__(self):
        super(AddLayersControlsForm, self).__init__()

        layout = QVBoxLayout(self)

        gbox_params = QGroupBox()
        layout.addWidget(gbox_params)
        self.params_form = QFormLayout()
        gbox_params.setLayout(self.params_form)

        self.relativeSizes = QComboBox()
        self.relativeSizes.addItems(["true", "false"])
        self.params_form.addRow("relativeSizes", self.relativeSizes)

        self.expansionRatio = QLineEdit()
        self.expansionRatio.setValidator(QDoubleValidator(0.0, 999999.0, 50))
        self.expansionRatio.setText("1.0")
        self.params_form.addRow("expansionRatio", self.expansionRatio)


        self.finalLayerThickness = QLineEdit()
        self.finalLayerThickness.setValidator(QDoubleValidator(0.0, 999999.0, 50))
        self.finalLayerThickness.setText("0.3")
        self.params_form.addRow("finalLayerThickness", self.finalLayerThickness)


        self.minThickness = QLineEdit()
        self.minThickness.setValidator(QDoubleValidator(0.0, 999999.0, 50))
        self.minThickness.setText("0.25")
        self.params_form.addRow("minThickness", self.minThickness)


        self.nGrow = QLineEdit("0")
        self.nGrow.setValidator(QIntValidator(0, 999999))
        self.params_form.addRow("nGrow", self.nGrow)


        self.featureAngle = QLineEdit("30")
        self.featureAngle.setValidator(QIntValidator(0, 360))
        self.params_form.addRow("featureAngle", self.featureAngle)


        self.nRelaxIter = QLineEdit("5")
        self.nRelaxIter.setValidator(QIntValidator(0, 999999))
        self.params_form.addRow("nRelaxIter", self.nRelaxIter)


        self.nSmoothSurfaceNormals = QLineEdit("1")
        self.nSmoothSurfaceNormals.setValidator(QIntValidator(0, 999999))
        self.params_form.addRow("nSmoothSurfaceNormals", self.nSmoothSurfaceNormals)


        self.nSmoothNormals = QLineEdit("3")
        self.nSmoothNormals.setValidator(QIntValidator(0, 999999))
        self.params_form.addRow("nSmoothNormals", self.nSmoothNormals)


        self.nSmoothThickness = QLineEdit("10")
        self.nSmoothThickness.setValidator(QIntValidator(0, 999999))
        self.params_form.addRow("nSmoothThickness", self.nSmoothThickness)


        self.maxFaceThicknessRatio = QLineEdit()
        self.maxFaceThicknessRatio.setValidator(QDoubleValidator(0.0, 999999.0, 50))
        self.maxFaceThicknessRatio.setText("0.5")
        self.params_form.addRow("maxFaceThicknessRatio", self.maxFaceThicknessRatio)


        self.maxThicknessToMedialRatio = QLineEdit()
        self.maxThicknessToMedialRatio.setValidator(QDoubleValidator(0.0, 999999.0, 50))
        self.maxThicknessToMedialRatio.setText("0.3")
        self.params_form.addRow("maxThicknessToMedialRatio", self.maxThicknessToMedialRatio)


        self.minMedianAxisAngle = QLineEdit("90")
        self.minMedianAxisAngle.setValidator(QIntValidator(0, 360))
        self.params_form.addRow("minMedianAxisAngle", self.minMedianAxisAngle)


        self.nBufferCellsNoExtrude = QLineEdit("0")
        self.nBufferCellsNoExtrude.setValidator(QIntValidator(0, 999999))
        self.params_form.addRow("nBufferCellsNoExtrude", self.nBufferCellsNoExtrude)


        self.nLayerIter = QLineEdit("50")
        self.nLayerIter.setValidator(QIntValidator(0, 999999))
        self.params_form.addRow("nLayerIter", self.nLayerIter)


        self.nRelaxedIter = QLineEdit("20")
        self.nRelaxedIter.setValidator(QIntValidator(0, 999999))
        self.params_form.addRow("nRelaxedIter", self.nRelaxedIter)



    def set_params(self, addLayersC):
        count = len(addLayersC)
        self.relativeSizes.setCurrentText(addLayersC[0][1])
        for row in range(1, count):
            self.params_form.itemAt(row, 1).widget().setText(addLayersC[row][1])


    def read_addLayersC_GUIdata(self):
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
