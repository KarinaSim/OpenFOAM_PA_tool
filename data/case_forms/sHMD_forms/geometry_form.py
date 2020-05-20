import re
import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QHBoxLayout, QComboBox, QLabel, \
    QApplication, QScrollArea, QPushButton, QFileDialog

from data.case_forms.sHMD_forms.new_region_dwin import RegionDialog
from data.case_forms.sHMD_forms.new_surface_dwin import SurfaceDialog


class GeometryForm(QWidget):

    del_surface_signal = pyqtSignal()

    def __init__(self, statusBar):
        super(GeometryForm, self).__init__()

        self.statusBar = statusBar

        self.surface_id = 0
        self.region_id = 0

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


        btn_hbox = QHBoxLayout()
        del_btn = QPushButton("Delete last surface")
        del_btn.clicked.connect(self.delete_surface)
        btn_hbox.addWidget(del_btn)
        add_btn = QPushButton("Add surface")
        add_btn.clicked.connect(self.new_surface)
        btn_hbox.addWidget(add_btn)
        vbox_surfaces.addLayout(btn_hbox)


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


        btn_hbox = QHBoxLayout()
        del_btn = QPushButton("Delete last region")
        del_btn.clicked.connect(self.delete_region)
        btn_hbox.addWidget(del_btn)
        add_btn = QPushButton("Add region")
        add_btn.clicked.connect(self.new_region)
        btn_hbox.addWidget(add_btn)
        vbox_regions.addLayout(btn_hbox)

        layout = QVBoxLayout(self)
        layout.addWidget(gbox_surfaces)
        layout.addWidget(gbox_regions)


        self.new_region_dialog = RegionDialog()
        self.new_region_dialog.new_region_signal.connect(self.new_region_signal_handler)

        self.new_surface_dialog = SurfaceDialog()
        self.new_surface_dialog.new_surface_signal.connect(self.new_surface_signal_handler)


    def new_region(self):
       self.new_region_dialog.show()

    def new_region_signal_handler(self, name):
        self.region_id += 1
        region = RefinementRegion(self.region_id, name)
        self.regions.addWidget(region)

    def new_surface(self):
       self.new_surface_dialog.show()

    def new_surface_signal_handler(self, name):
        self.surface_id += 1
        surface = RefinementSurface(self.surface_id, name, self.statusBar)
        self.surfaces.addWidget(surface)

    def set_geometry_connections(self, castellatedMC_form):
        self.castellatedMC_form = castellatedMC_form

    def delete_region(self):

       self.region_id -= 1
       last_region_num = self.regions.count()
       if last_region_num == 0:
           return
       self.regions.takeAt(last_region_num - 1).widget().deleteLater()
       self.castellatedMC_form.regions.takeAt(last_region_num - 1).widget().deleteLater()


    def delete_surface(self):

      self.surface_id -= 1
      last_surface_num = self.surfaces.count()
      if last_surface_num == 0:
          return
      self.surfaces.takeAt(last_surface_num - 1).widget().deleteLater()
      self.castellatedMC_form.surfaces.takeAt(last_surface_num - 1).widget().deleteLater()
      self.del_surface_signal.emit()




class RefinementSurface(QWidget):
    def __init__(self, id, name, statusBar):
        super(RefinementSurface, self).__init__()

        self.statusBar = statusBar

        self.surface_id = id
        self.filename = None
        self.stl_data = None

        vbox = QVBoxLayout(self)
        gbox = QGroupBox()
        vbox.addWidget(gbox)
        gbox_form = QFormLayout()
        gbox.setLayout(gbox_form)

        self.name = QLabel(name)
        self.type = QLabel("triSurfaceMesh")
        filename_hbox = QHBoxLayout()
        btn = QPushButton("...")
        btn.setFixedSize(40, 20)
        btn.clicked.connect(self.set_filename)
        self.file = QLabel()
        filename_hbox.addWidget(self.file)
        filename_hbox.addWidget(btn)

        gbox_form.addRow("Name", self.name)
        gbox_form.addRow("Type", self.type)
        gbox_form.addRow("File", filename_hbox)

    def set_surface(self, surface):
        name, typee, file, stl_data = surface
        self.name.setText(name)
        self.type.setText(typee)
        self.file.setText(file)
        self.filename = file.strip('"')
        self.stl_data = stl_data


    def set_filename(self):
        filepath = QFileDialog.getOpenFileName(self, "Выбрать файл", "/home", "STL files (*.stl)")[0]
        self.filename = re.search(r'([^\/]+).stl$', filepath).group()
        self.file.setText('"' + self.filename + '"')

        try:
            with open(filepath) as filehandler:
                self.stl_data = filehandler.read()
                self.statusBar.showMessage("Data " + self.filename + " loaded successfully", 2000)
        except IOError:
            self.statusBar.showMessage("Data " + self.filename + " IOError has occurred!", 3000)

    def get_stl_data(self):
        if self.file.text() == "" or self.file.text() is None:
            return [None, None]
        else:
            return [self.filename, self.stl_data]

    def read_surfaceGUIdata(self):
        return [self.name.text(), self.type.text(), self.file.text()]


class RefinementRegion(QWidget):
    def __init__(self, id, name):
        super(RefinementRegion, self).__init__()

        self.region_id = id

        vbox = QVBoxLayout(self)
        gbox = QGroupBox()
        vbox.addWidget(gbox)
        self.gbox_form = QFormLayout()
        gbox.setLayout(self.gbox_form)

        self.name = QLabel(name)
        self.type = QComboBox()
        self.type.addItems(["searchableSphere", "searchableBox"])
        self.type.currentTextChanged.connect(lambda text : self.set_params(text))


        self.gbox_form.addRow("Name", self.name)
        self.gbox_form.addRow("Type", self.type)

        self.centre_hbox = None
        self.radius = None
        self.min_hbox = None
        self.max_hbox = None


        centre, radius = self.searchableSphere_params()
        self.gbox_form.addRow("centre", centre)
        self.gbox_form.addRow("radius", radius)



    def set_region(self, region):
        name, typee, val1, val2 = region
        self.name.setText(name)
        self.type.setCurrentText(typee)
        if typee == "searchableSphere":
            for i in range(0, self.centre_hbox.count()):
                self.centre_hbox.itemAt(i).widget().setText(val1[i])
            self.radius.setText(val2)
        else:
            for i in range(0, self.min_hbox.count()):
                self.min_hbox.itemAt(i).widget().setText(val1[i])
                self.max_hbox.itemAt(i).widget().setText(val2[i])





    def read_regionGUIdata(self):
        name = self.name.text()
        type = self.type.currentText()
        val1 = []
        val2 = []

        coords = self.gbox_form.itemAt(2, 1).layout()
        for i in range(0, 3):
            coord = coords.itemAt(i).widget().text()
            val1.append(coord)
        val1 = " ".join(val1)
        val1 = "(" + val1 + ")"

        if type == 'searchableSphere':
            val2 = self.gbox_form.itemAt(3, 1).widget().text()
        elif type == 'searchableBox':
            coords = self.gbox_form.itemAt(3, 1).layout()
            for i in range(0, 3):
                coord = coords.itemAt(i).widget().text()
                val2.append(coord)
            val2 = " ".join(val2)
            val2 = "(" + val2 + ")"

        return [name, type, val1, val2]


    def set_params(self, text):
        if text == 'searchableSphere':
            if self.gbox_form.rowCount() == 4:
                self.gbox_form.removeRow(3)
                self.gbox_form.removeRow(2)
                centre, radius = self.searchableSphere_params()
                self.gbox_form.addRow("centre", centre)
                self.gbox_form.addRow("radius", radius)


        if text == 'searchableBox':
            if self.gbox_form.rowCount() == 4:
                self.gbox_form.removeRow(3)
                self.gbox_form.removeRow(2)
                min, max = self.searchableBox_params()
                self.gbox_form.addRow("min", min)
                self.gbox_form.addRow("max", max)


    def searchableSphere_params(self):

        self.centre_hbox = QHBoxLayout()
        self.centre_x = QLineEdit()
        self.centre_y = QLineEdit()
        self.centre_z = QLineEdit()
        self.centre_x.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        self.centre_y.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        self.centre_z.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        self.centre_x.setText("0.0")
        self.centre_y.setText("0.0")
        self.centre_z.setText("0.0")
        self.centre_hbox.addWidget(self.centre_x)
        self.centre_hbox.addWidget(self.centre_y)
        self.centre_hbox.addWidget(self.centre_z)

        self.radius = QLineEdit()
        self.radius.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        self.radius.setText("0.03")

        return [self.centre_hbox, self.radius]

    def searchableBox_params(self):

        self.min_hbox = QHBoxLayout()
        self.max_hbox = QHBoxLayout()


        self.min_x = QLineEdit()
        self.min_y = QLineEdit()
        self.min_z = QLineEdit()
        self.min_x.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        self.min_y.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        self.min_z.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        self.min_x.setText("-0.05")
        self.min_y.setText("-0.02")
        self.min_z.setText("-0.02")
        self.min_hbox.addWidget(self.min_x)
        self.min_hbox.addWidget(self.min_y)
        self.min_hbox.addWidget(self.min_z)

        self.max_x = QLineEdit()
        self.max_y = QLineEdit()
        self.max_z = QLineEdit()
        self.max_x.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        self.max_y.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        self.max_z.setValidator(QDoubleValidator(-999999.0, 999999.0, 50))
        self.max_x.setText("0.05")
        self.max_y.setText("0.02")
        self.max_z.setText("0.02")
        self.max_hbox.addWidget(self.max_x)
        self.max_hbox.addWidget(self.max_y)
        self.max_hbox.addWidget(self.max_z)

        return [self.min_hbox, self.max_hbox]


def main():
   app = QApplication(sys.argv)
   ex = GeometryForm()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
