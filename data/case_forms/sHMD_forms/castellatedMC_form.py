import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QHBoxLayout, QComboBox, \
    QScrollArea, QApplication, QLabel


class CastellatedMCForm(QWidget):

    def __init__(self):
        super(CastellatedMCForm, self).__init__()

        gbox_params = QGroupBox()
        self.params_form = QFormLayout()
        gbox_params.setLayout(self.params_form)

        self.maxLocalCells = QLineEdit()
        self.maxLocalCells.setValidator(QIntValidator(0, 9999999))
        self.maxLocalCells.setText("100000")
        self.params_form.addRow("maxLocalCells", self.maxLocalCells)


        self.maxGlobalCells = QLineEdit()
        self.maxGlobalCells.setValidator(QIntValidator(0, 9999999))
        self.maxGlobalCells.setText("2000000")
        self.params_form.addRow("maxGlobalCells", self.maxGlobalCells)


        self.minRefinementCells = QLineEdit()
        self.minRefinementCells.setValidator(QIntValidator(0, 9909999))
        self.minRefinementCells.setText("0")
        self.params_form.addRow("minRefinementCells", self.minRefinementCells)


        self.nCellsBetweenLevels = QLineEdit()
        self.nCellsBetweenLevels.setValidator(QIntValidator(0, 9990999))
        self.nCellsBetweenLevels.setText("1")
        self.params_form.addRow("nCellsBetweenLevels", self.nCellsBetweenLevels)


        self.resolveFeatureAngle = QLineEdit()
        self.resolveFeatureAngle.setValidator(QIntValidator(0, 360))
        self.resolveFeatureAngle.setText("30")
        self.params_form.addRow("resolveFeatureAngle", self.resolveFeatureAngle)


        self.locationInMesh = QHBoxLayout()
        self.locationInMesh.setSpacing(2)

        self.coord_x = QLineEdit()
        self.coord_y = QLineEdit()
        self.coord_z = QLineEdit()
        self.coord_x.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        self.coord_y.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        self.coord_z.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        self.coord_x.setText("0.07")
        self.coord_y.setText("0.04")
        self.coord_z.setText("0.03")
        self.locationInMesh.addWidget(self.coord_x)
        self.locationInMesh.addWidget(self.coord_y)
        self.locationInMesh.addWidget(self.coord_z)
        self.params_form.addRow("locationInMesh", self.locationInMesh)


        self.allowFreeStandingZoneFaces = QComboBox()
        self.allowFreeStandingZoneFaces.addItems(["true", "false"])
        self.params_form.addRow("allowFreeStandingZoneFaces", self.allowFreeStandingZoneFaces)


        self.surfaces = QVBoxLayout()
        self.surfaces.setAlignment(Qt.AlignVCenter | Qt.AlignTop)
        scroll1_widget = QWidget()
        scroll1_widget.setLayout(self.surfaces)
        scroll1 = QScrollArea()
        scroll1.setWidget(scroll1_widget)
        scroll1.setWidgetResizable(True)

        vbox_surfaces = QVBoxLayout()
        gbox_surfaces = QGroupBox("RefinementSurfaces")
        gbox_surfaces.setLayout(vbox_surfaces)
        vbox_surfaces.addWidget(scroll1)


        self.regions = QVBoxLayout()
        self.regions.setAlignment(Qt.AlignVCenter | Qt.AlignTop)
        scroll2_widget = QWidget()
        scroll2_widget.setLayout(self.regions)
        scroll2 = QScrollArea()
        scroll2.setWidget(scroll2_widget)
        scroll2.setWidgetResizable(True)

        vbox_regions = QVBoxLayout()
        gbox_regions = QGroupBox("RefinementRegions")
        gbox_regions.setLayout(vbox_regions)
        vbox_regions.addWidget(scroll2)

        layout = QVBoxLayout(self)
        layout.addWidget(gbox_params)
        layout.addWidget(gbox_surfaces)
        layout.addWidget(gbox_regions)


        self.show()


    def set_params(self, params):
       for row in range(0, 5):
           self.params_form.itemAt(row, 1).widget().setText(params[row][1])
       self.coord_x.setText(params[5][1][0])
       self.coord_y.setText(params[5][1][1])
       self.coord_z.setText(params[5][1][2])
       self.allowFreeStandingZoneFaces.setCurrentText(params[6][1])


    def read_castellatedGUI(self):
        params = []
        for row in range(0, 5):
            label = self.params_form.itemAt(row, 0).widget().text()
            value = self.params_form.itemAt(row, 1).widget().text()
            params.append([label, value])
        label = self.params_form.itemAt(5, 0).widget().text()
        value = [self.coord_x.text(), self.coord_y.text(), self.coord_z.text()]
        value = " ".join(value)
        value = "(" + value + ")"
        params.append([label, value])

        label = self.params_form.itemAt(6, 0).widget().text()
        value = self.allowFreeStandingZoneFaces.currentText()
        params.append([label, value])
        return params



    def create_region(self, name):
       region = RefinementRegion(name)
       self.regions.addWidget(region)

    def create_surface(self, name):
       surface = RefinementSurface(name)
       self.surfaces.addWidget(surface)


class RefinementSurface(QWidget):
    def __init__(self, name):
        super(RefinementSurface, self).__init__()


        vbox = QVBoxLayout(self)
        gbox = QGroupBox()
        vbox.addWidget(gbox)
        gbox_form = QFormLayout()
        gbox.setLayout(gbox_form)

        self.name = QLabel(name)
        level = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.setContentsMargins(100, 0, 0, 0)
        hbox.addWidget(QLabel("min"))
        hbox.addWidget(QLabel("max"))
        level.addLayout(hbox)
        self.level_hbox = QHBoxLayout()
        self.level_x = QLineEdit()
        self.level_y = QLineEdit()
        self.level_x.setValidator(QIntValidator(0, 999999))
        self.level_y.setValidator(QIntValidator(0, 999999))
        self.level_x.setText("5")
        self.level_y.setText("6")
        self.level_hbox.addWidget(self.level_x)
        self.level_hbox.addWidget(self.level_y)
        level.addLayout(self.level_hbox)

        gbox_form.addRow("Name", self.name)
        gbox_form.addRow("Level", level)


    def set_surface(self, surface):
        name, level = surface
        self.name.setText(name)
        self.level_x.setText(level[0])
        self.level_y.setText(level[1])


    def read_surfaceGUIdata(self):
        name = self.name.text()
        level = "(" + self.level_x.text() + " " + self.level_y.text() + ")"

        return [name, level]


class RefinementRegion(QWidget):
    def __init__(self, name):
        super(RefinementRegion, self).__init__()

        vbox = QVBoxLayout(self)
        gbox = QGroupBox()
        vbox.addWidget(gbox)
        self.gbox_form = QFormLayout()
        gbox.setLayout(self.gbox_form)

        self.name = QLabel(name)
        self.mode = QComboBox()
        self.mode.addItems(["inside", "outside", "distance"])
        self.mode.currentTextChanged.connect(lambda text : self.set_additlevel(text))
        self.levels = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.setContentsMargins(100, 0, 0, 0)
        hbox.addWidget(QLabel("min"))
        hbox.addWidget(QLabel("max"))
        self.levels.addLayout(hbox)
        self.add_level()

        self.gbox_form.addRow("Name", self.name)
        self.gbox_form.addRow("Type", self.mode)
        self.gbox_form.addRow("Levels", self.levels)



    def set_region(self, region):
        name, mode, levels = region
        self.name.setText(name)
        self.mode.setCurrentText(mode)
        if mode == "distance":
            for i in range(1, self.levels.count()):
                level_hbox = self.levels.itemAt(i).layout()
                level_hbox.itemAt(0).widget().setText(levels[i - 1][0])
                level_hbox.itemAt(1).widget().setText(levels[i - 1][1])
        else:
            level_hbox = self.levels.itemAt(1).layout()
            level_hbox.itemAt(0).widget().setText(levels[0])
            level_hbox.itemAt(1).widget().setText(levels[1])


    def set_additlevel(self, text):
        if text == 'distance':
            self.add_level()
        if text == 'inside' or text == 'outside':
            if self.levels.count() == 3:
                self.levels.itemAt(2).layout().itemAt(0).widget().deleteLater()
                self.levels.itemAt(2).layout().itemAt(1).widget().deleteLater()
                self.levels.itemAt(2).layout().deleteLater()


    def add_level(self):
        hbox = QHBoxLayout()
        x = QLineEdit()
        y = QLineEdit()
        x.setValidator(QDoubleValidator(0.0, 999999, 50))
        y.setValidator(QIntValidator(0, 999999))
        x.setText("1e15")
        y.setText("3")
        hbox.addWidget(x)
        hbox.addWidget(y)
        self.levels.addLayout(hbox)
        return hbox

    def read_regionGUIdata(self):
        name = self.name.text()
        mode = self.mode.currentText()
        levels = ""

        hbox = self.levels.itemAt(1).layout()
        l1 = hbox.itemAt(0).widget().text()
        l2 = hbox.itemAt(1).widget().text()
        levels = "((" + l1 + " " + l2 + "))"

        if mode == 'distance':
            hbox = self.levels.itemAt(2).layout()
            l1 = hbox.itemAt(0).widget().text()
            l2 = hbox.itemAt(1).widget().text()
            level = "(" + l1 + " " + l2 + ")"
            levels = "(" + levels + " "  + level + ")"

        return [name, mode, levels]


def main():
   app = QApplication(sys.argv)
   ex = CastellatedMCForm()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
