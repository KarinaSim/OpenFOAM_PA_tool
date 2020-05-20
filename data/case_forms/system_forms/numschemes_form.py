from PyQt5.QtWidgets import QWidget, QGroupBox, QComboBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFormLayout, \
    QLineEdit, QLabel, QVBoxLayout, QPushButton, QScrollArea

class NumschemesForm(QWidget):

   def __init__( self):
      super().__init__()

      self.numschemes_vbox = QVBoxLayout()
      self.numschemes_vbox.setAlignment(Qt.AlignVCenter | Qt.AlignTop)

      ddtSchemes_gbox = QGroupBox("ddtSchemes")
      self.ddtSchemes_form = QFormLayout()
      self.ddtSchemes_form.setSpacing(25)
      self.ddtSchemes_form.setVerticalSpacing(5)

      ddtSchemes_default = QComboBox()
      ddtSchemes_default.addItems(["steadyState", "Euler"])
      self.ddtSchemes_form.addRow("default", ddtSchemes_default)

      ddtSchemes_gbox.setLayout(self.ddtSchemes_form)



      gradSchemes_gbox = QGroupBox("gradSchemes")
      self.gradSchemes_form = QFormLayout()
      self.gradSchemes_form.setSpacing(25)
      self.gradSchemes_form.setVerticalSpacing(5)

      gradSchemes_default = QComboBox()
      gradSchemes_default.addItem("Gauss linear")
      self.gradSchemes_form.addRow("default", gradSchemes_default)


      gradSchemes_gbox.setLayout(self.gradSchemes_form)



      divSchemes_gbox = QGroupBox("divSchemes")
      self.divSchemes_form = QFormLayout()
      self.divSchemes_form.setSpacing(25)
      self.divSchemes_form.setVerticalSpacing(5)

      divSchemes_default = QComboBox()
      divSchemes_default.addItem("none")
      self.divSchemes_form.addRow("default", divSchemes_default)
      div = QComboBox()
      div.addItems(["bounded Gauss linear", "Gauss linear"])
      self.divSchemes_form.addRow("div(phi,U)", div)

      div = QComboBox()
      div.addItem("Gauss linear")
      self.divSchemes_form.addRow("div((nuEff*dev2(T(grad(U)))))", div)

      divSchemes_gbox.setLayout(self.divSchemes_form)



      laplacianSchemes_gbox = QGroupBox("laplacianSchemes")
      self.laplacianSchemes_form = QFormLayout()
      self.laplacianSchemes_form.setSpacing(25)
      self.laplacianSchemes_form.setVerticalSpacing(5)

      laplacianSchemes_default = QComboBox()
      laplacianSchemes_default.addItems(["Gauss linear corrected", "Gauss linear orthogonal"])
      self.laplacianSchemes_form.addRow("default", laplacianSchemes_default)

      laplacianSchemes_gbox.setLayout(self.laplacianSchemes_form)



      interpolationSchemes_gbox = QGroupBox("interpolationSchemes")
      self.interpolationSchemes_form = QFormLayout()
      self.interpolationSchemes_form.setSpacing(25)
      self.interpolationSchemes_form.setVerticalSpacing(5)

      interpolationSchemes_default = QComboBox()
      interpolationSchemes_default.addItem("linear")
      self.interpolationSchemes_form.addRow("default", interpolationSchemes_default)

      interpolationSchemes_gbox.setLayout(self.interpolationSchemes_form)



      snGradSchemes_gbox = QGroupBox("snGradSchemes")
      self.snGradSchemes_form = QFormLayout()
      self.snGradSchemes_form.setSpacing(25)
      self.snGradSchemes_form.setVerticalSpacing(5)

      snGradSchemes_default = QComboBox()
      snGradSchemes_default.addItems(["corrected", "linear"])
      self.snGradSchemes_form.addRow("default", snGradSchemes_default)

      snGradSchemes_gbox.setLayout(self.snGradSchemes_form)

      fluxRequired_gbox = QGroupBox("fluxRequired")
      self.fluxRequired_form = QFormLayout()
      self.fluxRequired_form.setSpacing(25)
      self.fluxRequired_form.setVerticalSpacing(5)

      fluxRequired_default = QComboBox()
      fluxRequired_default.addItems(["no"])
      self.fluxRequired_form.addRow("default", fluxRequired_default)

      fluxRequired_gbox.setLayout(self.fluxRequired_form)

      self.numschemes_vbox.addWidget(ddtSchemes_gbox)
      self.numschemes_vbox.addWidget(gradSchemes_gbox)
      self.numschemes_vbox.addWidget(divSchemes_gbox)
      self.numschemes_vbox.addWidget(laplacianSchemes_gbox)
      self.numschemes_vbox.addWidget(interpolationSchemes_gbox)
      self.numschemes_vbox.addWidget(snGradSchemes_gbox)
      self.numschemes_vbox.addWidget(fluxRequired_gbox)

      self.setLayout(self.numschemes_vbox)


   def set_params(self, params):
      ddtSchemes, gradSchemes, divSchemes, laplacianSchemes, \
      interpolationSchemes, snGradSchemes, fluxRequired = params

      for row in range(0, self.ddtSchemes_form.rowCount()):
         self.ddtSchemes_form.itemAt(row, 1).widget().setCurrentText(ddtSchemes[row][1])

      for row in range(0, self.gradSchemes_form.rowCount()):
         self.gradSchemes_form.itemAt(row, 1).widget().setCurrentText(gradSchemes[row][1])

      for row in range(0, self.divSchemes_form.rowCount()):
         self.divSchemes_form.itemAt(row, 1).widget().setCurrentText(divSchemes[row][1])

      for row in range(0, self.laplacianSchemes_form.rowCount()):
         self.laplacianSchemes_form.itemAt(row, 1).widget().setCurrentText(laplacianSchemes[row][1])

      for row in range(0, self.interpolationSchemes_form.rowCount()):
         self.interpolationSchemes_form.itemAt(row, 1).widget().setCurrentText(interpolationSchemes[row][1])

      for row in range(0, self.snGradSchemes_form.rowCount()):
         self.snGradSchemes_form.itemAt(row, 1).widget().setCurrentText(snGradSchemes[row][1])

      for row in range(0, self.fluxRequired_form.rowCount()):
         self.fluxRequired_form.itemAt(row, 1).widget().setCurrentText(fluxRequired[row][1])





   def read_numschemesGUIdata(self):
      numschemes = {}

      for item in range(0, self.numschemes_vbox.count()):
         groupbox = self.numschemes_vbox.itemAt(item).widget()
         groupbox_name = groupbox.title()
         form = groupbox.layout()
         label_value_list = []
         for row in range(0, form.rowCount()):
            label = form.itemAt(row, 0).widget().text()
            value = form.itemAt(row, 1).widget().currentText()
            label_value_list.append([label, value])
         numschemes.update({groupbox_name : label_value_list})
      return numschemes
