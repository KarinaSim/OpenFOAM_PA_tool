from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QComboBox, QLineEdit, QScrollArea, QWidget, QFormLayout, QVBoxLayout


class RuntimeForm(QWidget):

    def __init__(self):
        super(RuntimeForm, self).__init__()

        layout = QVBoxLayout(self)
        self.form = QFormLayout()

        scroll_widget = QWidget()
        scroll_widget.setLayout(self.form)
        scroll = QScrollArea()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)

        self.application = QComboBox(self)
        self.application.addItems(["simpleFoam"]) # , "simpleFoam", "laplacianFoam", "pisoFoam"
        self.form.addRow("application", self.application)

        self.startFrom = QComboBox(self)
        self.startFrom.addItems(["startTime"]) # , "firstTime", "latestTime"
        self.form.addRow("startFrom", self.startFrom)

        self.startFrom_option = QLineEdit("0")
        self.startFrom_option.setValidator(QDoubleValidator(0.0, 999999.0, 10))
        self.form.addRow("startTime", self.startFrom_option)

        self.stopAt = QComboBox(self)
        self.stopAt.addItems(["endTime"]) # , "writeNow", "noWriteNow", "nextWrite"
        self.form.addRow("stopAt", self.stopAt)

        self.stopAt_option = QLineEdit("1000")
        self.stopAt_option.setValidator(QDoubleValidator(0.0, 999999.0, 10))
        self.form.addRow("endTime", self.stopAt_option)

        self.deltaT = QLineEdit("1")
        self.deltaT.setValidator(QDoubleValidator(0.0, 999999.0, 10))
        self.form.addRow("deltaT", self.deltaT)

        self.writeControl = QComboBox(self)
        self.writeControl.addItems(["runTime", "timeStep", "adjustableRunTime","cpuTime", "clockTime"])
        self.form.addRow("writeControl", self.writeControl)

        self.writeInterval = QLineEdit("50")
        self.writeInterval.setValidator(QDoubleValidator(0.0, 999999.0, 10))
        self.form.addRow("writeInterval", self.writeInterval)

        self.purgeWrite = QLineEdit("0")
        self.purgeWrite.setValidator(QIntValidator(0, 999999))
        self.form.addRow("purgeWrite", self.purgeWrite)

        self.writeFormat = QComboBox(self)
        self.writeFormat.addItems(["ascii", "binary"])
        self.form.addRow("writeFormat", self.writeFormat)

        self.writeFormat_option = QLineEdit("6")
        self.writeFormat_option.setValidator(QIntValidator(0, 999999))
        self.form.addRow("writePrecision", self.writeFormat_option)

        self.writeCompression = QComboBox(self)
        self.writeCompression.addItems(["off", "on"])
        self.form.addRow("writeCompression", self.writeCompression)

        self.timeFormat = QComboBox(self)
        self.timeFormat.addItems(["general", "fixed", "scientific"])
        self.form.addRow("timeFormat", self.timeFormat)

        self.timeFormat_option = QLineEdit("6")
        self.timeFormat_option.setValidator(QIntValidator(0, 999999))
        self.form.addRow("timePrecision", self.timeFormat_option)

        self.runTimeModifiable = QComboBox(self)
        self.runTimeModifiable.addItems(["true", "false"])
        self.form.addRow("runTimeModifiable", self.runTimeModifiable)

        layout.addWidget(scroll)


    def set_params(self, params):

        self.application.setCurrentText(params[0][1])
        self.startFrom.setCurrentText(params[1][1])
        self.startFrom_option.setText(params[2][1])
        self.stopAt.setCurrentText(params[3][1])
        self.stopAt_option.setText(params[4][1])
        self.deltaT.setText(params[5][1])
        self.writeControl.setCurrentText(params[6][1])
        self.writeInterval.setText(params[7][1])
        self.purgeWrite.setText(params[8][1])
        self.writeFormat.setCurrentText(params[9][1])
        self.writeFormat_option.setText(params[10][1])
        self.writeCompression.setCurrentText(params[11][1])
        self.timeFormat.setCurrentText(params[12][1])
        self.timeFormat_option.setText(params[13][1])
        self.runTimeModifiable.setCurrentText(params[14][1])




    def read_runtime_GUIdata(self):
        runtime = []
        for row in range(0, self.form.rowCount()):
            label = self.form.itemAt(row, 0).widget().text()
            value = self.form.itemAt(row, 1).widget()
            if isinstance(value, QComboBox):
                value = value.currentText()
            else:
                value = value.text()
            runtime.append([label, value])
        return runtime
