from PyQt5.QtWidgets import QWidget, QGroupBox, QComboBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFormLayout, \
    QLineEdit, QLabel, QVBoxLayout, QPushButton, QScrollArea

class SolcontrolForm(QWidget):


   def __init__( self):
      super().__init__()

      self.solcontrol_vbox = QVBoxLayout()
      self.solcontrol_vbox.setAlignment(Qt.AlignVCenter | Qt.AlignTop)

      simple_gbox = QGroupBox()
      simple_form = QFormLayout()
      simple_form.setSpacing(25)
      simple_form.setVerticalSpacing(5)
      simple_gbox.setLayout(simple_form)

      simple = QComboBox()
      simple.addItem("SIMPLE")
      simple_form.addRow("Algorithm", simple)

      self.nNonOrthogonalCorrectors = QLineEdit("0")
      self.nNonOrthogonalCorrectors.setValidator(QIntValidator(0, 999999))
      simple_form.addRow("nNonOrthogonalCorrectors", self.nNonOrthogonalCorrectors)

      residualControl_vbox = QVBoxLayout()
      residualControl_form = QFormLayout()
      residualControl_form.setSpacing(20)
      residualControl_form.setVerticalSpacing(5)
      residualControl_vbox.addLayout(residualControl_form)
      self.simple_p = QLineEdit("1e-5")
      self.simple_p.setValidator(QDoubleValidator(0.0, 999999.0, 50))
      residualControl_form.addRow("p", self.simple_p)
      self.simple_U = QLineEdit("1e-5")
      self.simple_U.setValidator(QDoubleValidator(0.0, 999999.0, 50))
      residualControl_form.addRow("U", self.simple_U)

      simple_form.addRow("residualControl", residualControl_vbox)




      p_gbox = QGroupBox("p")
      p_form = QFormLayout()
      p_form.setSpacing(25)
      p_form.setVerticalSpacing(5)

      self.psolver = QComboBox()
      self.psolver.addItems(["GAMG", "PCG"])
      p_form.addRow("solver", self.psolver)

      self.psmoother = QComboBox()
      self.psmoother.addItems(["GaussSeidel"])
      p_form.addRow("smoother", self.psmoother)

      self.ptolerance = QLineEdit("1e-07")
      self.ptolerance.setValidator(QDoubleValidator(0.0, 999999.0, 50))
      p_form.addRow("tolerance", self.ptolerance)
      self.prelTol = QLineEdit()
      self.prelTol.setValidator(QDoubleValidator(0.0, 999999.0, 50))
      self.prelTol.setText("0.01")
      p_form.addRow("relTol", self.prelTol)

      p_gbox.setLayout(p_form)



      U_gbox = QGroupBox("U")
      U_form = QFormLayout()
      U_form.setSpacing(25)
      U_form.setVerticalSpacing(5)

      self.Usolver = QComboBox()
      self.Usolver.addItems(["PBiCGStab", "smoothSolver"])
      U_form.addRow("solver", self.Usolver)
      self.preconditioner = QComboBox()
      self.preconditioner.addItem("DILU")
      U_form.addRow("preconditioner", self.preconditioner)
      self.Utolerance = QLineEdit("1e-08")
      self.Utolerance.setValidator(QDoubleValidator(0.0, 999999.0, 50))
      U_form.addRow("tolerance", self.Utolerance)
      self.UrelTol = QLineEdit("0")
      self.UrelTol.setValidator(QDoubleValidator(0.0, 999999.0, 50))
      U_form.addRow("relTol", self.UrelTol)

      U_gbox.setLayout(U_form)


      relaxationFactors_gbox = QGroupBox("relaxationFactors")
      relaxationFactors_vbox = QVBoxLayout()
      relaxationFactors_vbox.setSpacing(25)
      relaxationFactors_gbox.setLayout(relaxationFactors_vbox)

      fields_gbox = QGroupBox("fields")
      fields_hbox = QHBoxLayout()
      fields_hbox.setSpacing(25)
      fields_gbox.setLayout(fields_hbox)
      relaxationFactors_vbox.addWidget(fields_gbox)

      self.p = QLineEdit()
      self.p.setValidator(QDoubleValidator(0.0, 999999.0, 50))
      self.p.setText("0.3")
      fields_hbox.addWidget(QLabel("p"))
      fields_hbox.addWidget(self.p)

      equations_gbox = QGroupBox("equations")
      equations_hbox = QHBoxLayout()
      equations_hbox.setSpacing(25)
      equations_gbox.setLayout(equations_hbox)
      relaxationFactors_vbox.addWidget(equations_gbox)

      self.U = QLineEdit()
      self.U.setValidator(QDoubleValidator(0.0, 999999.0, 50))
      self.U.setText("0.5")
      equations_hbox.addWidget(QLabel("U"))
      equations_hbox.addWidget(self.U)



      self.solcontrol_vbox.addWidget(p_gbox)
      self.solcontrol_vbox.addWidget(U_gbox)
      self.solcontrol_vbox.addWidget(simple_gbox)
      self.solcontrol_vbox.addWidget(relaxationFactors_gbox)

      self.setLayout(self.solcontrol_vbox)


   def set_params(self, params):
       p, U, SIMPLE, relaxationFactors = params

       self.psolver.setCurrentText(p[0][1])
       self.psmoother.setCurrentText(p[1][1])
       self.ptolerance.setText(p[2][1])
       self.prelTol.setText(p[3][1])

       self.Usolver.setCurrentText(U[0][1])
       self.preconditioner.setCurrentText(U[1][1])
       self.Utolerance.setText(U[2][1])
       self.UrelTol.setText(U[3][1])

       self.nNonOrthogonalCorrectors.setText(SIMPLE[0][1])
       self.simple_p.setText(SIMPLE[1][1])
       self.simple_U.setText(SIMPLE[2][1])

       self.p.setText(relaxationFactors[0][1])
       self.U.setText(relaxationFactors[1][1])


   def read_solcontrolGUI(self):
      solcontrol = {}

      for item in range(0, 2):
         groupbox = self.solcontrol_vbox.itemAt(item).widget()
         groupbox_name = groupbox.title()
         form = groupbox.layout()
         label_value_list = []
         for row in range(0, form.rowCount()):
            label = form.itemAt(row, 0).widget().text()
            value = form.itemAt(row, 1).widget()
            if isinstance(value, QComboBox):
                value = value.currentText()
            else:
                value = value.text()
            label_value_list.append([label, value])
         solcontrol.update({groupbox_name : label_value_list})

      slabel_value_list = []
      slabel_value_list.append(["nNonOrthogonalCorrectors", self.nNonOrthogonalCorrectors.text()])
      slabel_value_list.append(["p", self.simple_p.text()])
      slabel_value_list.append(["U", self.simple_U.text()])
      solcontrol.update({"SIMPLE" : slabel_value_list})

      label_value_list = []
      label_value_list.append(["p", self.p.text()])
      label_value_list.append(["U", self.U.text()])
      solcontrol.update({"relaxationFactors" : label_value_list})
      return solcontrol
