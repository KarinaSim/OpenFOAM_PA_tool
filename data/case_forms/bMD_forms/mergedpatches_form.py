import re

from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QLabel, QSpinBox, \
    QFormLayout, QGroupBox, QPushButton, QScrollArea, QVBoxLayout, QComboBox, QGridLayout


class MergedPatchesForm(QWidget):

   def __init__( self):
      super().__init__()

      self.merged_patches = QVBoxLayout()
      self.merged_patches.setAlignment(Qt.AlignVCenter | Qt.AlignTop)

      scroll_widget = QWidget()
      scroll_widget.setLayout(self.merged_patches)
      scroll = QScrollArea()
      scroll.setWidget(scroll_widget)
      scroll.setWidgetResizable(True)

      layout = QVBoxLayout(self)
      layout.addWidget(scroll)

   def create_merged_patches(self, master_patches, slave_patches):
       block_merged_patches = MergedPatches(master_patches, slave_patches)
       self.merged_patches.addWidget(block_merged_patches)


class MergedPatches(QWidget):
    def __init__( self, master_patches, slave_patches):
      super().__init__()

      self.master_patches = master_patches
      self.slave_patches = slave_patches


      layout = QVBoxLayout(self)
      merged_patches = QGroupBox()
      layout.addWidget(merged_patches)

      self.grid = QGridLayout()
      self.grid.setVerticalSpacing(5)
      merged_patches.setLayout(self.grid)
      self.grid.addWidget(QLabel("Master patch"), 0, 0)
      self.grid.addWidget(QLabel("Slave patch"), 0, 1)

      master_patch = QComboBox()
      master = [str(item) for item in self.master_patches]
      master_patch.addItems(master)
      self.grid.addWidget(master_patch, 1, 0)

      slave_patch = QComboBox()
      slave = [str(item) for item in self.slave_patches]
      slave_patch.addItems(slave)
      self.grid.addWidget(slave_patch, 1, 1)


    def set_mergedPatches(self, mergePatchPairs):
        master, slave = mergePatchPairs
        self.grid.itemAtPosition(1, 0).widget().setCurrentText(master)
        self.grid.itemAtPosition(1, 1).widget().setCurrentText(slave)



    def read_block_merged_patchesGUIdata(self):
        master_slave_list = []
        for row in range(1, self.grid.rowCount()):
            item = self.grid.itemAtPosition(row, 0).widget()
            master = item.currentText()
            item = self.grid.itemAtPosition(row, 1).widget()
            slave = item.currentText()
            master_slave_list.append((master, slave))
            master_slave_list = [str(m) for m in master_slave_list]
            master_slave_list = [re.sub(r"[',]", "", v) for v in master_slave_list]
        return master_slave_list

