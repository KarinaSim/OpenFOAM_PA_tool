import sys

from PyQt5.QtWidgets import QWidget, QGroupBox, QComboBox, QGridLayout, QApplication
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFormLayout, \
    QLineEdit, QLabel, QVBoxLayout, QPushButton, QScrollArea

class InitialCondsForm(QWidget):


   def __init__( self):
      super().__init__()

      self.blocks_pU = QVBoxLayout(self)
      self.blocks_pU.setAlignment(Qt.AlignVCenter | Qt.AlignTop)

      hbox = QHBoxLayout()
      hbox.setSpacing(50)
      hbox.setAlignment(Qt.AlignVCenter)
      hbox.setContentsMargins(10, 0, 10, 0)
      internalField_p_vbox = QVBoxLayout()
      internalField_p_vbox.setSpacing(2)
      internalField_p_vbox.addWidget(QLabel("Internal field pressure (m2/c2)"))
      self.if_p = QLineEdit()
      self.if_p.setValidator(QDoubleValidator(0.0, 999999.0, 50))
      self.if_p.setText("0")
      internalField_p_vbox.addWidget(self.if_p)


      internalField_U_vbox = QVBoxLayout()
      internalField_U_vbox.setSpacing(2)
      internalField_U_vbox.addWidget(QLabel("Internal field velocity (m/c)"))
      if_U_hbox = QHBoxLayout()
      if_U_hbox.setSpacing(2)
      self.if_xU = QLineEdit()
      self.if_xU.setValidator(QDoubleValidator(0.0, 999999.0, 50))
      self.if_xU.setText("0")
      self.if_yU = QLineEdit()
      self.if_yU.setValidator(QDoubleValidator(0.0, 999999.0, 50))
      self.if_yU.setText("0")
      self.if_zU = QLineEdit()
      self.if_zU.setValidator(QDoubleValidator(0.0, 999999.0, 50))
      self.if_zU.setText("0")
      if_U_hbox.addWidget(self.if_xU)
      if_U_hbox.addWidget(self.if_yU)
      if_U_hbox.addWidget(self.if_zU)
      internalField_U_vbox.addLayout(if_U_hbox)

      hbox.addLayout(internalField_p_vbox)
      hbox.addLayout(internalField_U_vbox)

      scroll_widget = QWidget()
      scroll_widget.setLayout(self.blocks_pU)
      scroll = QScrollArea()
      scroll.setWidget(scroll_widget)
      scroll.setWidgetResizable(True)

      self.layout = QVBoxLayout(self)
      self.layout.setSpacing(2)
      self.layout.addLayout(hbox)
      self.layout.addWidget(scroll)

      self.surfaces_form = None

      self.add_counter = 0

   def create_block_pU(self, pnames):
       block_pU = BlockPU(pnames)
       self.blocks_pU.addWidget(block_pU)
       return  block_pU


   def add_sHMD_surface(self, name):
       self.add_counter += 1
       if self.add_counter == 1:
           self.set_surface_form()
       block0_pU = self.blocks_pU.itemAt(0).widget()
       patch_hbox = block0_pU.get_patch_hbox()
       self.surfaces_form.addRow(QLabel(name), patch_hbox)

   def delete_sHMD_surface(self):
       self.add_counter -= 1
       if self.add_counter == 0:
           self.layout.itemAt(2).widget().deleteLater()
           self.surfaces_form = None
       else:
           self.surfaces_form.removeRow(self.add_counter)

   def delete_surfaces_form(self):
       if self.surfaces_form is not None:
           self.add_counter = 0
           self.layout.itemAt(2).widget().deleteLater()
           self.surfaces_form = None
       else:
           return


   def set_surfaces(self, surfaces_p, surfaces_U):

        for row in range(1, self.surfaces_form.rowCount()):
            self.surfaces_form.itemAt(row, 0).widget().setText(surfaces_p[row - 1][0])
            p = surfaces_p[row - 1][1]
            patch_hbox = self.surfaces_form.itemAt(row, 1).layout()
            p_tv_vbox = patch_hbox.itemAt(1).layout()
            if type(p) == str:
                p_tv_vbox.itemAt(0).widget().setCurrentText(p)
            else:
                p_tv_vbox.itemAt(0).widget().setCurrentText(p[0])
                p_tv_vbox.itemAt(1).widget().setText(p[1])

            U = surfaces_U[row - 1][1]
            U_tv_vbox = patch_hbox.itemAt(2).layout()
            if type(U) == str:
                U_tv_vbox.itemAt(0).widget().setCurrentText(U)
            else:
                U_tv_vbox.itemAt(0).widget().setCurrentText(U[0])
                Uvalue = U_tv_vbox.itemAt(1).layout()
                value = U[1].strip("()").split(" ")
                for i in range(0, Uvalue.count()):
                    Uvalue.itemAt(i).widget().setText(value[i])


   def read_GUIdata_surface(self, form):

        pnames = []

        p_type_value_list = []
        U_type_value_list = []

        for row in range(1, form.rowCount()):

            pname = form.itemAt(row, 0).widget().text()
            pnames.append(pname)
            patch_hbox = form.itemAt(row, 1).layout()

            p_tv_vbox = patch_hbox.itemAt(1).layout()
            ptype = p_tv_vbox.itemAt(0).widget()
            ptype = ptype.currentText()
            if ptype == "fixedValue":
                pvalue = p_tv_vbox.itemAt(1).widget().text().replace(',', '.')
                p_type_value_list.append([ptype, pvalue])
            else:
                p_type_value_list.append(ptype)

            U_tv_vbox = patch_hbox.itemAt(2).layout()
            Utype = U_tv_vbox.itemAt(0).widget()
            Utype = Utype.currentText()
            if Utype == "fixedValue":
                Uvalue = U_tv_vbox.itemAt(1).layout()
                coords = []
                for c in range(0, 3):
                    coord = Uvalue.itemAt(c).widget().text().replace(',', '.')
                    print(coord)
                    coords.append(coord)
                coords = " ".join(coords)
                coords = "(" + coords + ")"
                U_type_value_list.append([Utype, coords])
            else:
                U_type_value_list.append(Utype)

        patches_p = list(zip(pnames, p_type_value_list))
        patches_U = list(zip(pnames, U_type_value_list))

        return [patches_p, patches_U]


   def set_surface_form(self):
       self.surfaces_form = QFormLayout()
       self.surfaces_form.setVerticalSpacing(20)
       self.surfaces_form.setSpacing(70)

       tophbox = QHBoxLayout()
       tophbox.addWidget(QLabel(""))
       tophbox.addWidget(QLabel("Pressure (m2/c2)"))
       tophbox.addWidget(QLabel("Velocity (m/c)"))
       self.surfaces_form.addRow("Patch", tophbox)

       scroll_widget2 = QWidget()
       scroll_widget2.setLayout(self.surfaces_form)
       scroll2 = QScrollArea()
       scroll2.setWidget(scroll_widget2)
       scroll2.setWidgetResizable(True)

       self.layout.addWidget(scroll2)


class BlockPU(QWidget):
    def __init__( self, pnames):
      super().__init__()

      self.pnames = pnames

      layout = QVBoxLayout(self)
      block_pU = QGroupBox("Boundary field")
      layout.addWidget(block_pU)

      self.block_pU_form = QFormLayout()
      self.block_pU_form.setSpacing(70)
      self.block_pU_form.setVerticalSpacing(20)
      block_pU.setLayout(self.block_pU_form)

      tophbox = QHBoxLayout()
      tophbox.addWidget(QLabel(""))
      tophbox.addWidget(QLabel("Pressure (m2/c2)"))
      tophbox.addWidget(QLabel("Velocity (m/c)"))
      self.block_pU_form.addRow("Patch", tophbox)


      for row in range(1, 7):
          patch_hbox = self.get_patch_hbox()

          self.block_pU_form.addRow(QLabel(self.pnames[row - 1]), patch_hbox)



    def get_patch_hbox(self):
          patch_hbox = QHBoxLayout()
          patch_hbox.setSpacing(50)

          tv_vbox =QVBoxLayout()
          tv_vbox.setSpacing(2)
          tv_vbox.addWidget(QLabel("type"))
          tv_vbox.addWidget(QLabel("value"))
          patch_hbox.addLayout(tv_vbox)

          p_tv_vbox = QVBoxLayout()
          p_tv_vbox.setSpacing(2)
          ptype = QComboBox()
          ptype.addItems(["empty", "fixedValue", "zeroGradient"])
          pvalue = QLineEdit()
          pvalue.setValidator(QDoubleValidator(-999999, 999999, 50))


          # Сигнал о выборе другого значения в комбобоксе
          ptype.currentTextChanged.connect(lambda text, edt=pvalue: edt.setEnabled(text == "fixedValue"))
          # Установим изначальную доступность pvalue
          pvalue.setEnabled(ptype.currentText() == "fixedValue")

          p_tv_vbox.addWidget(ptype)
          p_tv_vbox.addWidget(pvalue)
          patch_hbox.addLayout(p_tv_vbox)


          U_tv_vbox = QVBoxLayout()
          U_tv_vbox.setSpacing(2)
          Utype = QComboBox()
          Utype.addItems(["zeroGradient","noSlip", "fixedValue", "empty", "slip"])
          Uvalue = QHBoxLayout()
          xU = QLineEdit()
          yU = QLineEdit()
          zU = QLineEdit()
          xU.setEnabled(False)
          yU.setEnabled(False)
          zU.setEnabled(False)
          xU.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
          yU.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
          zU.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))

          Utype.currentTextChanged.connect(                                             # +++
                lambda text, x=xU, y = yU, z = zU: self.change_Uvalue(text, x, y, z))    # +++

          Uvalue.addWidget(xU)
          Uvalue.addWidget(yU)
          Uvalue.addWidget(zU)

          U_tv_vbox.addWidget(Utype)
          U_tv_vbox.addLayout(Uvalue)
          patch_hbox.addLayout(U_tv_vbox)

          return patch_hbox


    def set_initialconds(self, p_boundaryField, U_boundaryField):

        for k, v in U_boundaryField.items():
            if p_boundaryField.get(k):
                p_boundaryField[k] = [p_boundaryField[k], v]
        boundary = p_boundaryField
        pnames = list(boundary.keys())
        pU = list(boundary.values())
        for row in range(1, 7):
            self.block_pU_form.itemAt(row, 0).widget().setText(pnames[row - 1])
            p, U = pU[row - 1]
            patch_hbox = self.block_pU_form.itemAt(row, 1).layout()
            p_tv_vbox = patch_hbox.itemAt(1).layout()
            if type(p) == str:
                p_tv_vbox.itemAt(0).widget().setCurrentText(p)
            else:
                p_tv_vbox.itemAt(0).widget().setCurrentText(p[0])
                p_tv_vbox.itemAt(1).widget().setText(p[1])

            U_tv_vbox = patch_hbox.itemAt(2).layout()
            if type(U) == str:
                U_tv_vbox.itemAt(0).widget().setCurrentText(U)
            else:
                U_tv_vbox.itemAt(0).widget().setCurrentText(U[0])
                Uvalue = U_tv_vbox.itemAt(1).layout()
                value = U[1].strip("()").split(" ")
                for i in range(0, Uvalue.count()):
                    Uvalue.itemAt(i).widget().setText(value[i])



    def update_pnames(self, pnames):
        self.pnames = pnames
        print(pnames)
        for row in range(2, 8):
            pname = self.block_pU_form.itemAt(row, 0).widget()
            pname.setText(self.pnames[row - 2])


    def change_Uvalue(self, text, xU, yU, zU):                               # +++
        if text == 'fixedValue':
            xU.setEnabled(True)
            yU.setEnabled(True)
            zU.setEnabled(True)

        else:
            xU.setEnabled(False)
            yU.setEnabled(False)
            zU.setEnabled(False)


    def read_block_pUGUIdata(self):
        pnames = []

        p_type_value_list = []
        U_type_value_list = []

        for row in range(1, self.block_pU_form.rowCount()):

            pname = self.block_pU_form.itemAt(row, 0).widget().text()
            pnames.append(pname)
            patch_hbox = self.block_pU_form.itemAt(row, 1).layout()

            p_tv_vbox = patch_hbox.itemAt(1).layout()
            ptype = p_tv_vbox.itemAt(0).widget()
            ptype = ptype.currentText()
            if ptype == "fixedValue":
                pvalue = p_tv_vbox.itemAt(1).widget().text().replace(',', '.')
                p_type_value_list.append([ptype, pvalue])
            else:
                p_type_value_list.append(ptype)

            U_tv_vbox = patch_hbox.itemAt(2).layout()
            Utype = U_tv_vbox.itemAt(0).widget()
            Utype = Utype.currentText()
            if Utype == "fixedValue":
                Uvalue = U_tv_vbox.itemAt(1).layout()
                coords = []
                for c in range(0, 3):
                    coord = Uvalue.itemAt(c).widget().text().replace(',', '.')
                    print(coord)
                    coords.append(coord)
                coords = " ".join(coords)
                coords = "(" + coords + ")"
                U_type_value_list.append([Utype, coords])
            else:
                U_type_value_list.append(Utype)

        patches_p = dict(zip(pnames, p_type_value_list))
        patches_U = dict(zip(pnames, U_type_value_list))


        return [patches_p, patches_U]
