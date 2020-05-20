import sys

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget, QVBoxLayout, QPushButton, QGroupBox, QScrollArea, QGridLayout, \
    QComboBox, QApplication


class PatchesForm(QWidget):

    def __init__(self):
        super(PatchesForm, self).__init__()


        self.blocks_patches = QVBoxLayout()
        self.blocks_patches.setAlignment(Qt.AlignVCenter | Qt.AlignTop)

        scroll_widget = QWidget()
        scroll_widget.setLayout(self.blocks_patches)
        scroll = QScrollArea()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)


    def create_block_patches(self, pnames, block_pU, patches):
        block_patches = BlockPatches(pnames, block_pU, patches)
        self.blocks_patches.addWidget(block_patches)


class BlockPatches(QWidget):

    def __init__(self, pnames, block_pU, patches):
        super(BlockPatches, self).__init__()

        self.patches = patches
        self.block_pU = block_pU
        self.pnames = pnames

        layout = QVBoxLayout(self)
        block_patches = QGroupBox()
        layout.addWidget(block_patches)
        inner_vbox = QVBoxLayout()
        block_patches.setLayout(inner_vbox)

        self.grid = QGridLayout()
        self.grid.setVerticalSpacing(5)
        self.grid.setHorizontalSpacing(100)
        inner_vbox.addLayout(self.grid)

        self.grid.addWidget(QLabel("Patch"), 0, 0)
        self.grid.addWidget(QLabel("Name"), 0, 1)
        self.grid.addWidget(QLabel("Type"), 0, 2)

        # set_pnames_btn = QPushButton("Set names")
        # set_pnames_btn.clicked.connect(self.send_pnames)
        # inner_vbox.addWidget(set_pnames_btn)


        for row in range(1, 7):
            patch = QLabel(str(patches[row - 1]))
            self.grid.addWidget(patch, row , 0)
            name = QLabel(self.pnames[row - 1])
            self.grid.addWidget(name, row, 1)
            type = QComboBox()
            type.addItems(["empty", "wall"])
            self.grid.addWidget(type, row, 2)


    def set_types(self, patchestypes):
        pnames = list(patchestypes.keys())
        types_patches = list(patchestypes.values())

        for row in range(1, 7):
            self.grid.itemAtPosition(row, 0).widget().setText(types_patches[row - 1][1])
            self.grid.itemAtPosition(row, 1).widget().setText(pnames[row - 1])
            self.grid.itemAtPosition(row, 2).widget().setCurrentText(types_patches[row - 1][0])

    def send_pnames(self):
        self.pnames.clear()
        for row in range(1, 7):
            item = self.grid.itemAtPosition(row, 1).widget()
            name = item.text()
            self.pnames.append(name)
        self.block_pU.update_pnames(self.pnames)


    def read_block_patchesGUIdata(self):
        names = self.pnames
        patches = self.patches
        types = []
        for row in range(1, 7):
            item = self.grid.itemAtPosition(row, 2).widget()
            type = item.currentText()
            types.append(type)

        types_patches = [[t, p] for t, p in zip(types, patches)]
        names_types_patches = dict(zip(names, types_patches))
        return  names_types_patches


def main():
   app = QApplication(sys.argv)
   ex = PatchesForm()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
